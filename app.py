"""
app.py
------
Main entry point for the SmartStudy AI Streamlit application.

HOW IT WORKS:
  - Streamlit renders this file as a web page.
  - A sidebar lets students pick which feature they want to use.
  - Each feature section calls the matching function in ai_helper.py.
  - If the API key is missing, we show a clear warning instead of crashing.

RUN THIS FILE WITH:
    streamlit run app.py
"""

import streamlit as st
from ai_helper import explain_topic, summarize_notes, explain_code, generate_quiz
from utils import api_key_is_configured, format_response, word_count

# ── Page configuration (must be the very first Streamlit call) ─────────────
st.set_page_config(
    page_title="SmartStudy AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — clean, modern look ────────────────────────────────────────
st.markdown(
    """
    <style>
        /* Overall background */
        .stApp { background-color: #f0f4f8; }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(160deg, #1e3a5f 0%, #2d6a9f 100%);
        }
        [data-testid="stSidebar"] * { color: #ffffff !important; }

        /* Feature cards */
        .feature-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 28px 32px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            margin-bottom: 24px;
        }

        /* Result box */
        .result-box {
            background: #eef6ff;
            border-left: 4px solid #2d6a9f;
            border-radius: 8px;
            padding: 20px 24px;
            margin-top: 16px;
            white-space: pre-wrap;
            font-size: 0.95rem;
            line-height: 1.7;
        }

        /* Stat pill */
        .stat-pill {
            display: inline-block;
            background: #d1e8ff;
            color: #1e3a5f;
            border-radius: 20px;
            padding: 2px 14px;
            font-size: 0.8rem;
            margin-top: 8px;
        }

        /* Headings */
        h1, h2, h3 { color: #1e3a5f; }

        /* Warning box */
        .api-warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Helper: show a friendly warning when the API key is missing ────────────
def show_api_warning():
    st.markdown(
        """
        <div class="api-warning">
            ⚠️ <strong>API Key Not Configured</strong><br>
            This feature needs a Gemini API key to work.<br>
            Please follow the instructions in <code>README.md</code> to add your
            key to the <code>.env</code> file, then restart the app.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Helper: display the AI response in a styled box ───────────────────────
def show_result(text: str):
    cleaned = format_response(text)
    wc = word_count(cleaned)
    st.markdown(
        f'<div class="result-box">{cleaned}</div>'
        f'<span class="stat-pill">📝 {wc} words</span>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════
#  SIDEBAR — Navigation
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎓 SmartStudy AI")
    st.markdown("*Your personal AI study assistant*")
    st.markdown("---")

    page = st.radio(
        "Choose a feature:",
        options=[
            "🏠  Home",
            "💡  Explain a Topic",
            "📄  Summarize Notes",
            "🐍  Code Explainer",
            "📝  Practice Quiz",
        ],
    )

    st.markdown("---")
    # Show a live API key status indicator in the sidebar
    if api_key_is_configured():
        st.success("✅ API Key configured")
    else:
        st.error("❌ API Key missing")

    st.markdown(
        "<small>Powered by Google Gemini</small>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════
if page == "🏠  Home":
    st.markdown("# 🎓 Welcome to SmartStudy AI")
    st.markdown(
        "**SmartStudy AI** is your personal, AI-powered study companion. "
        "Pick any feature from the sidebar to get started!"
    )

    # Feature overview cards laid out in a 2×2 grid
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>💡 Explain a Topic</h3>
                <p>Type any subject — from <em>recursion</em> to <em>photosynthesis</em> —
                and get a clear, beginner-friendly explanation with real-world analogies.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="feature-card">
                <h3>🐍 Code Explainer</h3>
                <p>Paste any Python snippet and receive a <strong>line-by-line</strong>
                breakdown in plain English — perfect for understanding code you copied
                or wrote yourself.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>📄 Summarize Notes</h3>
                <p>Paste your raw study notes and get back a <strong>concise summary</strong>,
                a bullet list of key points, and important vocabulary to review.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="feature-card">
                <h3>📝 Practice Quiz</h3>
                <p>Enter any topic and instantly generate a <strong>multiple-choice quiz</strong>
                with answers — great for testing yourself before an exam.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # API key status reminder on the home page
    if not api_key_is_configured():
        show_api_warning()
    else:
        st.info(
            "✅ Your API key is configured. All features are ready to use. "
            "Pick a feature from the sidebar to begin!"
        )


# ══════════════════════════════════════════════════════════════════════════
#  PAGE: EXPLAIN A TOPIC
# ══════════════════════════════════════════════════════════════════════════
elif page == "💡  Explain a Topic":
    st.markdown("# 💡 Explain a Topic")
    st.markdown(
        "Enter any concept or subject below and the AI will explain it "
        "in simple, beginner-friendly language with everyday analogies."
    )

    topic = st.text_input(
        "📌 What topic do you want to understand?",
        placeholder="e.g. How does a for loop work?  /  What is machine learning?",
    )

    if st.button("✨ Explain it to me", use_container_width=True):
        if not api_key_is_configured():
            show_api_warning()
        elif not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("🤔 Thinking..."):
                try:
                    result = explain_topic(topic)
                    st.success("Here's your explanation:")
                    show_result(result)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")


# ══════════════════════════════════════════════════════════════════════════
#  PAGE: SUMMARIZE NOTES
# ══════════════════════════════════════════════════════════════════════════
elif page == "📄  Summarize Notes":
    st.markdown("# 📄 Summarize Notes")
    st.markdown(
        "Paste your study notes below. The AI will produce a concise summary, "
        "key bullet points, and vocabulary to review."
    )

    notes = st.text_area(
        "📋 Paste your notes here:",
        height=280,
        placeholder="Paste any lecture notes, textbook paragraphs, or your own notes here…",
    )

    if st.button("📝 Summarize my notes", use_container_width=True):
        if not api_key_is_configured():
            show_api_warning()
        elif not notes.strip():
            st.warning("Please paste some notes first.")
        elif word_count(notes) < 20:
            st.warning("Your notes seem very short. Please paste at least a paragraph.")
        else:
            with st.spinner("📖 Reading your notes..."):
                try:
                    result = summarize_notes(notes)
                    st.success("Here's your summary:")
                    show_result(result)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")


# ══════════════════════════════════════════════════════════════════════════
#  PAGE: CODE EXPLAINER
# ══════════════════════════════════════════════════════════════════════════
elif page == "🐍  Code Explainer":
    st.markdown("# 🐍 Python Code Explainer")
    st.markdown(
        "Paste any Python code below. The AI will walk through it "
        "**line by line** in plain English."
    )

    code = st.text_area(
        "💻 Paste your Python code here:",
        height=280,
        placeholder="# Example:\nfor i in range(5):\n    print(i)",
    )

    if st.button("🔍 Explain this code", use_container_width=True):
        if not api_key_is_configured():
            show_api_warning()
        elif not code.strip():
            st.warning("Please paste some code first.")
        else:
            with st.spinner("🔎 Analysing your code..."):
                try:
                    result = explain_code(code)
                    st.success("Here's your line-by-line explanation:")
                    show_result(result)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")


# ══════════════════════════════════════════════════════════════════════════
#  PAGE: PRACTICE QUIZ
# ══════════════════════════════════════════════════════════════════════════
elif page == "📝  Practice Quiz":
    st.markdown("# 📝 Practice Quiz Generator")
    st.markdown(
        "Enter any topic and choose how many questions you want. "
        "The AI will generate a multiple-choice quiz with answers."
    )

    quiz_topic = st.text_input(
        "🎯 Quiz topic:",
        placeholder="e.g. Python lists  /  Variables  /  Object-oriented programming",
    )

    num_q = st.slider(
        "How many questions?",
        min_value=3,
        max_value=10,
        value=5,
        step=1,
    )

    if st.button("🎲 Generate Quiz", use_container_width=True):
        if not api_key_is_configured():
            show_api_warning()
        elif not quiz_topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner(f"🎓 Creating {num_q} questions on '{quiz_topic}'..."):
                try:
                    result = generate_quiz(quiz_topic, num_q)
                    st.success(f"Your {num_q}-question quiz on **{quiz_topic}**:")
                    show_result(result)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
