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
:root {
    --bg: #0b1220;
    --card: #0f172a;
    --card-2: #111827;
    --border: #1f2937;
    --text-muted: #94a3b8;
    --accent: #7c3aed;
}
.big-title {font-size:44px; font-weight:900; letter-spacing:-0.02em;}
.subtext {color: var(--text-muted); margin-top:-6px;}
.card {background-color:var(--card); padding:16px; border-radius:14px; margin-bottom:12px; border: 1px solid var(--border);}
.card-glow {background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(56,189,248,0.08)); border: 1px solid rgba(124,58,237,0.3);} 
.pill {display:inline-block; padding:4px 10px; border-radius:999px; background:var(--card-2); border:1px solid #334155; font-size:12px; margin-right:6px; color:#e2e8f0;}
.muted {color: var(--text-muted);}
.section-title {font-size:20px; font-weight:700; margin: 8px 0 4px 0;}
.kpi {background:var(--card); border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;}
.kpi-label {color: var(--text-muted); font-size:12px;}
.kpi-value {font-size:22px; font-weight:800;}
.badge {display:inline-block; padding:2px 8px; border-radius:6px; background:#1f2937; border:1px solid #334155; font-size:11px; color:#e2e8f0; margin-left:6px;}
.resource {padding:12px; border:1px solid var(--border); border-radius:10px; margin-bottom:10px; background:var(--card-2);} 
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚙️ System Status")
    gemini_set = bool(os.getenv("GEMINI_API_KEY"))
    qdrant_url = os.getenv("QDRANT_URL")
    st.markdown(f"**Gemini API**: {'✅ Set' if gemini_set else '⚠️ Not set'}")
    st.markdown(f"**Qdrant URL**: {'✅ Set' if qdrant_url else '⚠️ Not set'}")
    st.markdown("---")
    st.markdown("## 💡 Tips")
    st.markdown("- Be specific about the mistake you made")
    st.markdown("- Add the core concept (e.g., recursion, TCP, DP)")
    st.markdown("- Keep it short and concrete")
    st.markdown("---")
    st.markdown("## 🔒 Privacy")
    st.caption("Your input is stored as learning events to improve future recommendations.")

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
        <div class="card card-glow">
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
            with col_a:
                st.markdown("<div class='kpi'><div class='kpi-label'>Weak Concepts</div><div class='kpi-value'>{}</div></div>".format(len(result["weak_concepts"])), unsafe_allow_html=True)
            with col_b:
                st.markdown("<div class='kpi'><div class='kpi-label'>Similar Mistakes</div><div class='kpi-value'>{}</div></div>".format(len(result["similar_mistakes"])), unsafe_allow_html=True)
            with col_c:
                st.markdown("<div class='kpi'><div class='kpi-label'>Strategy</div><div class='kpi-value'>{}</div></div>".format(result["task_type"].upper()), unsafe_allow_html=True)

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
                with st.expander("View similar mistakes"):
                    for e in result["similar_mistakes"]:
                        st.write("•", e["text"])
            else:
                st.write("No similar mistakes found.")

            st.markdown("### 📚 Recommended Resources")
            if result.get("resources"):
                for r in result["resources"]:
                    text_value = r.get("text", "")
                    concept_value = r.get("concept", "")
                    topic_value = r.get("topic", "")
                    st.markdown(
                        f"<div class='resource'><div>{text_value}</div>"
                        f"<div class='muted' style='margin-top:6px;'>"
                        f"{concept_value}"
                        f"<span class='badge'>{topic_value}</span>"
                        f"</div></div>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No resources found yet. Add more to the knowledge base.")

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
