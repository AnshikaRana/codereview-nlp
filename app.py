import streamlit as st
import pandas as pd
import base64

# -------------------------------
# SAFE MODULE IMPORTS
# -------------------------------
IMPORT_ERRORS = []

try:
    from modules.name_quality import analyze_names
except Exception as e:
    analyze_names = None
    IMPORT_ERRORS.append(f"name_quality: {e}")

try:
    from modules.comment_quality import analyze_comments
except Exception as e:
    analyze_comments = None
    IMPORT_ERRORS.append(f"comment_quality: {e}")

try:
    from modules.commit_scorer import score_commit
except Exception as e:
    score_commit = None
    IMPORT_ERRORS.append(f"commit_scorer: {e}")

try:
    from modules.sentiment import analyze_sentiment
except Exception as e:
    analyze_sentiment = None
    IMPORT_ERRORS.append(f"sentiment: {e}")

    if IMPORT_ERRORS:
        st.error("Some modules failed to load:")
    for err in IMPORT_ERRORS:
        st.write(err)
# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="CodeReview NLP",
    page_icon="💎",
    layout="wide"
)

# -------------------------------
# BACKGROUND UI
# -------------------------------
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    try:
        bin_str = get_base64(png_file)

        st.markdown(
            f"""
            <style>

            .stApp {{
                background:
                radial-gradient(circle at center,
                rgba(10,10,42,0.45) 0%,
                rgba(0,0,0,0.96) 100%),
                url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}

            /* --- THE FIX FOR TRANSPARENT BOXES --- */
            div[data-baseweb="textarea"],
            div[data-baseweb="input"],
            div[data-baseweb="base-input"],
            .stTextArea textarea,
            .stTextInput input {{
                background-color: transparent !important; /* Force transparency */
                background: transparent !important;       /* Extra safety */
                color: white !important;
                border-radius: 14px !important;
                border: 1px solid rgba(255,255,255,0.12) !important;
                backdrop-filter: blur(12px) !important;
            }}

            /* Removes the shadow/inner-grey layer from Streamlit boxes */
            div[data-testid="stMarkdownContainer"] {{
                background: transparent !important;
            }}

            .stButton > button {{
                width: 100%;
                height: 4rem;
                border-radius: 14px;
                border: none;
                font-size: 1.2rem;
                font-weight: 800;
                color: white;
                background: linear-gradient(135deg,#ff4b2b,#ffb400);
                box-shadow: 0 10px 20px rgba(255,140,0,0.25);
                transition: 0.25s ease;
            }}

            .stButton > button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 15px 25px rgba(255,180,0,0.4);
            }}

            [data-testid="stMetricValue"] {{
                color: #ffb400 !important;
                text-shadow: 0 0 8px rgba(255,180,0,0.25);
            }}

            [data-testid="stAlert"] {{
                background-color: rgba(255,255,255,0.05) !important;
                border-radius: 12px !important;
                backdrop-filter: blur(10px) !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except:
        st.warning("Background image not found.")

set_background("gradient background.jpg")

# -------------------------------
# TITLE
# -------------------------------
st.markdown(
    """
    <h1 style='font-size: 4.5rem; font-weight: 900; color: white; margin-bottom: 0px;'>
    CodeReview NLP
    </h1>
    """, 
    unsafe_allow_html=True
)
st.title("Automated PR Language & Documentation Quality Analyzer")
st.markdown(
    """
    <p style='font-size: 1.6rem; color: rgba(255, 255, 255, 0.7); font-style: italic;'>
    A Natural Language Processing system that evaluates the linguistic quality of code reviews, 
    commit messages, and inline comments using multi-model NLP pipeline
    </p>
    """, 
    unsafe_allow_html=True
)
st.divider()

# -------------------------------
# INPUT SECTION
# -------------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("📥 PR Data Input")

    code_input = st.text_area(
        "Paste Code + Comments",
        height=320,
        placeholder="Paste PR code here..."
    )

    commit_input = st.text_input(
        "Commit Message",
        placeholder="e.g. Fix login timeout bug"
    )

    reviews_input = st.text_area(
        "Review Comments (One per line)",
        height=170,
        placeholder="Looks good\nNeed timeout handling"
    )

with right:
    st.subheader("⚙️ Configuration")

    st.info("Modules Integrated:\n\n✅ Name Quality\n✅ Comment Quality\n✅ Commit Quality\n✅ Sentiment Analysis")

    st.warning("Ensure requirements installed & modules folder present.")

    analyze_btn = st.button("🚀 Analyze PR Health")

# -------------------------------
# HELPER FUNCTION
# -------------------------------
def realistic_score(score, flags):
    """
    Prevent unrealistic 100s
    """
    if score == 100 and len(flags) == 0:
        return 96
    elif score >= 95:
        return 94
    return score


# -------------------------------
# ANALYSIS LOGIC
# -------------------------------
if analyze_btn:

    if not code_input.strip():
        st.error("Please enter code first.")
        st.stop()

    with st.spinner("Analyzing PR quality..."):

        try:
            # Run Modules
            res_names = analyze_names(code_input)
            res_comments = analyze_comments(code_input)
            res_commit = score_commit(commit_input)

            review_list = [
                r.strip()
                for r in reviews_input.split("\n")
                if r.strip()
            ]

            res_sentiment = analyze_sentiment(review_list)

            results = [
                res_names,
                res_comments,
                res_commit,
                res_sentiment
            ]

            # Apply realistic caps
            for r in results:
                r["score"] = realistic_score(
                    r["score"],
                    r.get("flags", [])
                )

            # Overall
            avg_score = round(
                sum(r["score"] for r in results) / 4
            )

            # -------------------------
            # RESULTS HEADER
            # -------------------------
            st.divider()
            st.header("📊 Analysis Results")

            # Metrics
            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Name Quality", f"{res_names['score']}%")
            c2.metric("Comment Quality", f"{res_comments['score']}%")
            c3.metric("Commit Score", f"{res_commit['score']}%")
            c4.metric("Sentiment", f"{res_sentiment['score']}%")

            st.progress(avg_score / 100)
            st.subheader(f"Overall Health: {avg_score}%")

            # -------------------------
            # QUALITY BADGE
            # -------------------------
            if avg_score >= 90:
                st.success("🚀 Excellent Pull Request Quality")
            elif avg_score >= 75:
                st.info("✅ Good Pull Request Quality")
            elif avg_score >= 60:
                st.warning("⚠️ Moderate Pull Request Quality")
            else:
                st.error("❌ Needs Improvement")

            # -------------------------
            # CHART
            # -------------------------
            chart_df = pd.DataFrame({
                "Module": [
                    "Name",
                    "Comment",
                    "Commit",
                    "Sentiment"
                ],
                "Score": [
                    res_names["score"],
                    res_comments["score"],
                    res_commit["score"],
                    res_sentiment["score"]
                ]
            })

            st.subheader("📈 Module Scores Comparison")
            st.bar_chart(chart_df.set_index("Module"))

            with st.expander("📋 Detailed Score Table"):
                st.dataframe(chart_df, use_container_width=True)

            # -------------------------
            # FLAGS & SUGGESTIONS
            # -------------------------
            colA, colB = st.columns(2)

            with colA:
                st.subheader("🚩 Flags")

                total_flags = 0

                for r in results:
                    for flag in r.get("flags", []):
                        total_flags += 1
                        st.warning(
                            f"**{r['module'].upper()}**: {flag}"
                        )

                if total_flags == 0:
                    st.success("No major issues found.")

            with colB:
                st.subheader("💡 Suggestions")

                total_sugs = 0

                for r in results:
                    for sug in r.get("suggestions", []):
                        total_sugs += 1
                        st.info(
                            f"**{r['module'].upper()}**: {sug}"
                        )

                if total_sugs == 0:
                    st.success("Looks production-ready.")

        except Exception as e:
            st.error(f"Analysis failed: {e}")