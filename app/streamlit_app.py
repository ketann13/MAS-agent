import os
import sys

import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")
if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

from mas_learning_agent.agents.planner_agent import handle_student_input
from mas_learning_agent.agents.retrieval_agent import store_new_resource, store_feedback

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RecallAI",
    layout="wide",
    page_icon="🎓"
)

# ---------------- HEADER ----------------
st.markdown("""
<style>
.big-title {font-size:42px; font-weight:800;}
.subtext {color: #9aa0a6; margin-top:-6px;}
.card {background-color:#111827; padding:16px; border-radius:12px; margin-bottom:12px; border: 1px solid #1f2937;}
.pill {display:inline-block; padding:4px 10px; border-radius:999px; background:#111827; border:1px solid #374151; font-size:12px; margin-right:6px;}
.muted {color:#9aa0a6;}
.section-title {font-size:20px; font-weight:700; margin: 8px 0 4px 0;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚙️ System Status")
    gemini_set = bool(os.getenv("GEMINI_API_KEY"))
    qdrant_url = os.getenv("QDRANT_URL")
    st.markdown(f"**Gemini API**: {'Set' if gemini_set else '⚠️ Not set'}")
    st.markdown(f"**Qdrant URL**: {'Set' if qdrant_url else '⚠️ Not set'}")
    st.markdown("---")
    st.markdown("## 💡 Tips")
    st.markdown("- Be specific about the mistake you made")
    st.markdown("- Add the core concept (e.g., recursion, TCP, DP)")

st.info("⏳ Initializing AI models... first load can take 20–30 seconds.")

st.markdown('<div class="big-title">RecallAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">AI-powered personalized tutor with long-term memory</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.subheader("Enter Your Learning Issue")

col_input, col_preview = st.columns([2, 1], gap="large")

with col_input:
    text = st.text_area(
        "Describe your doubt or mistake",
        height=140,
        placeholder="e.g., I used binary search on an unsorted array and got wrong answers"
    )
    concept = st.text_input(
        "Related concept (e.g., recursion, TCP, DP)",
        placeholder="e.g., binary search"
    )

    action_col, reset_col = st.columns([1, 1])
    with action_col:
        submit = st.button("Get Personalized Help", use_container_width=True)
    with reset_col:
        reset = st.button("♻️ Reset", use_container_width=True)

    if reset:
        st.session_state.clear()
        st.rerun()

with col_preview:
    st.markdown("<div class='section-title'> What you'll get</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
      <div class="muted">Personalized output includes</div>
      <div style="margin-top:8px;">
        <span class="pill">Weak concepts</span>
        <span class="pill">Study strategy</span>
        <span class="pill">Similar mistakes</span>
        <span class="pill">Resources</span>
        <span class="pill">AI tutor</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- MAIN PIPELINE ----------------
if submit:
    if text.strip() == "" or concept.strip() == "":
        st.warning("Please enter both doubt and concept.")
    else:
        with st.spinner("Multi-Agent System analyzing your learning history..."):
            result = handle_student_input(text, concept, correct=False)

        st.markdown("---")

        tab_summary, tab_analysis, tab_ai, tab_transparency, tab_feedback = st.tabs(
            ["Summary", "Analysis", "AI Tutor", "Transparency", "Feedback"]
        )

        with tab_summary:
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Weak Concepts", len(result["weak_concepts"]))
            col_b.metric("Similar Mistakes", len(result["similar_mistakes"]))
            col_c.metric("Strategy", result["task_type"].upper())

            st.markdown("### Recommendations")
            if result.get("advice"):
                for tip in result["advice"]:
                    st.success(tip)
            else:
                st.info("No recommendations available yet.")

        # ================= ANALYSIS =================
        with tab_analysis:
            st.markdown("### 📌 Weak Concepts Detected")
            if result["weak_concepts"]:
                for c in result["weak_concepts"]:
                    st.warning(c)
            else:
                st.success("No weak concepts detected yet.")

            st.markdown("### Similar Past Mistakes")
            if result["similar_mistakes"]:
                for e in result["similar_mistakes"]:
                    st.write("•", e["text"])
            else:
                st.write("No similar mistakes found.")

        # ================= AI TUTOR =================
        with tab_ai:
            if result.get("ai_explanation"):
                st.markdown(result["ai_explanation"])
            else:
                st.info("AI explanation temporarily unavailable. Please rely on agent recommendations above.")

        # ================= AGENT TRANSPARENCY =================
        with tab_transparency:
            st.markdown("### Agents Involved")
            for a in result["agents_used"]:
                st.write("✅", a)

            st.markdown("###  Reasoning Based On")
            if result["similar_mistakes"]:
                for e in result["similar_mistakes"]:
                    st.write(f"- Similar past mistake related to **{e['concept']}**")
            else:
                st.write("No prior mistakes found.")

        # ================= FEEDBACK LOOP =================
        with tab_feedback:
            st.subheader("Help the System Learn")

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
