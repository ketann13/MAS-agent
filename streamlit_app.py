import streamlit as st
from agents.planner_agent import handle_student_input
from agents.retrieval_agent import store_feedback, store_new_resource
from qdrant_db.client import get_qdrant_client


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Learning Memory Agent",
    layout="centered",
    page_icon="🎓"
)

# ---------------- QDRANT CONNECTION CHECK ----------------
qdrant_client = get_qdrant_client()
if qdrant_client is None:
    st.warning("⚠️ Memory database (Qdrant) is offline. The app will continue to work but without long-term memory features.")

# ---------------- HEADER ----------------
st.markdown("""
<style>
.big-title {font-size:40px; font-weight:700;}
.subtext {color: #9aa0a6;}
.card {background-color:#111827; padding:16px; border-radius:12px; margin-bottom:12px;}
</style>
""", unsafe_allow_html=True)

st.info("⏳ Initializing AI models... please wait 20–30 seconds on first load.")

st.markdown('<div class="big-title">🎓 AI Learning Memory Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Multi-Agent Personalized Tutor with Long-Term Memory (Qdrant)</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.subheader("📝 Enter Your Learning Issue")

text = st.text_area("Describe your doubt or mistake", height=120)
concept = st.text_input("Related concept (e.g., recursion, TCP, DP)")

submit = st.button("🚀 Get Personalized Help")

# ---------------- MAIN PIPELINE ----------------
if submit:
    if text.strip() == "" or concept.strip() == "":
        st.warning("Please enter both doubt and concept.")
    else:
        with st.spinner("🤖 Multi-Agent System analyzing your learning history..."):
            result = handle_student_input(text, concept, correct=False)

        st.markdown("---")

        # ================= ANALYSIS =================
        with st.expander("🧠 Analysis", expanded=True):

            st.markdown("### 📌 Weak Concepts Detected")
            if result["weak_concepts"]:
                for c in result["weak_concepts"]:
                    st.warning(c)
            else:
                st.success("No weak concepts detected yet.")

            st.markdown("### 🧭 Learning Strategy")
            st.info(f"**{result['task_type'].upper()}**")

            st.markdown("### 🧠 Similar Past Mistakes")
            if result["similar_mistakes"]:
                for e in result["similar_mistakes"]:
                    st.write("•", e["text"])
            else:
                st.write("No similar mistakes found.")

        # ================= RESOURCES =================
        st.subheader("🧠 What You Usually Struggle With")

        for c in result["weak_concepts"]:
            st.warning(c)


        # ================= AI TUTOR =================
        with st.expander("🤖 AI Tutor Explanation", expanded=True):

            if result.get("ai_explanation"):
                st.markdown(result["ai_explanation"])
            else:
                st.info("AI explanation temporarily unavailable. Please rely on agent recommendations above.")

        # ================= AGENT TRANSPARENCY =================
        with st.expander("🔍 Transparency: Why this recommendation?"):

            st.markdown("### 🤖 Agents Involved")
            for a in result["agents_used"]:
                st.write("✅", a)

            st.markdown("### 🧠 Reasoning Based On")
            for e in result["similar_mistakes"]:
                st.write(f"- Similar past mistake related to **{e['concept']}**")

        # ================= FEEDBACK LOOP =================
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

                if result["resources"]:
                    auto_text = result["resources"][0]["text"]
                    store_new_resource(auto_text, concept)

                st.success("✅ Helpful knowledge saved to long-term memory!")

            else:
                store_feedback(text, concept, False)
                st.warning("⚠ Feedback recorded. System will adapt next time.")
