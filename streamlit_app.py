import streamlit as st

from agents.planner_agent import handle_student_input
from agents.retrieval_agent import store_new_resource, store_feedback

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Learning Memory Agent", layout="centered")

st.info("⏳ Initializing AI models... please wait 20–30 seconds on first load.")

st.title("🎓 AI Learning Memory Agent")
st.write("Personalized AI tutor with long-term memory using Qdrant")

st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.subheader("📝 Enter Your Learning Issue")

text = st.text_area("Describe your doubt or mistake:")

concept = st.text_input("Related concept (e.g., recursion, binary search, DP)")

submit = st.button("Get Personalized Help")

# ---------------- MAIN PIPELINE ----------------
if submit:
    if text.strip() == "" or concept.strip() == "":
        st.warning("Please enter both doubt and concept.")
    else:
        with st.spinner("Analyzing your learning history using multi-agent system..."):
            result = handle_student_input(text, concept, correct=False)

        st.markdown("---")

        # -------- SIMILAR MISTAKES --------
        st.subheader("🧠 Similar Past Mistakes (From Memory)")
        if result["similar_mistakes"]:
            for e in result["similar_mistakes"]:
                st.write("•", e["text"])
        else:
            st.write("No similar past mistakes found.")

        # -------- WEAK CONCEPTS --------
        st.subheader("📌 Detected Weak Concepts")
        if result["weak_concepts"]:
            for c in result["weak_concepts"]:
                st.write("•", c)
        else:
            st.write("No weak concepts detected yet.")

        # -------- TASK ROUTING --------
        st.markdown("---")
        st.info(f"🧭 Learning Strategy Selected: **{result['task_type'].upper()}**")

        # -------- RESOURCES --------
        st.subheader("📚 Recommended Learning Resources")
        if result["resources"]:
            for r in result["resources"]:
                st.write("•", r["text"])
        else:
            st.write("No resources found.")

        # -------- ADVICE --------
        st.subheader("🎯 Personalized Advice")
        for a in result["advice"]:
            st.success(a)

        # -------- AGENT TRANSPARENCY --------
        st.markdown("---")
        st.subheader("🤖 Agents Involved in This Decision")

        for a in result["agents_used"]:
            st.write("✅", a)

        # -------- FEEDBACK LOOP --------
        st.markdown("---")
        st.subheader("🧠 Help the System Learn")

        feedback = st.radio(
            "Was this recommendation helpful?",
            ["Yes, it helped", "No, it didn’t help"],
            horizontal=True
        )

        confirm = st.button("Submit Feedback")

        if confirm:
            if feedback == "Yes, it helped":
                store_feedback(text, concept, True)

                # Store actual useful explanation into knowledge base
                if result["resources"]:
                    auto_text = result["resources"][0]["text"]
                    store_new_resource(auto_text, concept)

                st.success("Thanks! Helpful knowledge added to system memory.")

            else:
                store_feedback(text, concept, False)
                st.warning("Thanks! We'll improve recommendations for this topic.")

        # -------- TRACEABILITY --------
        st.markdown("---")
        st.subheader("🔍 Why This Recommendation?")

        st.write("Recommendations are based on your learning history:")

        for e in result["similar_mistakes"]:
            st.write(f"- Similar past mistake related to **{e['concept']}**")

