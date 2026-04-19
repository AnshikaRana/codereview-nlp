import streamlit as st
import pandas as pd
import base64
import os

# --- 1. NLP MODULE IMPORTS ---
try:
    from modules.name_quality import analyze_names
    from modules.comment_quality import analyze_comments
    from modules.commit_scorer import score_commit
    from modules.sentiment import analyze_sentiment
except ImportError as e:
    st.error(f"❌ Module Import Error: {e}")

# --- 2. GLASS UI ENGINE ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    try:
        bin_str = get_base64(png_file)
        page_bg_img = f'''
        <style>
        .stApp {{
            background: 
                radial-gradient(circle at center, rgba(10, 10, 42, 0.4) 0%, rgba(0, 0, 0, 0.95) 100%),
                url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}

        /* --- 100% TRANSPARENT INPUT BOXES --- */
        /* Targets the outer div and the inner textarea/input */
        div[data-baseweb="textarea"], 
        div[data-baseweb="input"], 
        div[data-baseweb="base-input"],
        .stTextArea textarea, 
        .stTextInput input {{
            background-color: transparent !important; /* Removes the grey completely */
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(8px) !important;
            transition: all 0.3s ease;
        }}

        /* Subtle glow on focus */
        .stTextArea textarea:focus, .stTextInput input:focus {{
            border: 1px solid #ffaa00 !important;
            box-shadow: 0 0 10px rgba(255, 170, 0, 0.2) !important;
        }}

        /* --- CONFIGURATION ALERTS --- */
        [data-testid="stAlert"] {{
            background-color: rgba(255, 255, 255, 0.05) !important; 
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(12px) !important;
            margin-bottom: 10px !important;
        }}
        [data-testid="stAlert"] * {{ color: white !important; }}

        /* --- BIG SUNSET GRADIENT BUTTON --- */
        .stButton {{
            display: flex;
            justify-content: center;
            margin-top: 25px;
        }}

        .stButton>button {{
            width: 100% !important;
            height: 5rem !important; /* Even bigger height */
            /* Gradient from Dark Orange to Vibrant Yellow */
            background: linear-gradient(135deg, #ff4b2b 0%, #ffb400 100%) !important;
            border-radius: 15px !important; /* Slightly more modern square-round */
            color: white !important;
            font-weight: 900 !important;
            font-size: 1.4rem !important; /* Very big text */
            text-transform: uppercase !important;
            letter-spacing: 3px !important;
            border: none !important;
            box-shadow: 0 10px 20px rgba(255, 75, 43, 0.3) !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }}

        .stButton>button:hover {{
            transform: translateY(-5px) scale(1.02) !important;
            box-shadow: 0 15px 30px rgba(255, 180, 0, 0.5) !important;
            filter: brightness(1.1);
        }}

        .stButton>button:active {{
            transform: translateY(2px) !important;
        }}

        [data-testid="stMetricValue"] {{
            color: #ffb400 !important;
            text-shadow: 0 0 10px rgba(255, 180, 0, 0.3) !important;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except:
        st.warning("Ensure 'gradient background.jpg' is in the folder.")

# --- 3. APP EXECUTION ---
st.set_page_config(page_title='CodeGlass NLP', layout='wide')
set_background('gradient background.jpg')

st.title('[Code Health Dashboard]')
st.markdown('**A professional tool for analyzing code, comments, and sentiment in PRs.**')
st.divider()

col_input, col_config = st.columns([2, 1])

with col_input:
    st.subheader('PR Data Input')
    code_input = st.text_area('Paste your Code & Comments here...', height=300)
    commit_input = st.text_input('Commit Message')
    reviews_input = st.text_area('Review Comments (One per line)', height=150)

with col_config:
    st.subheader('Configuration')
    st.write("") 
    st.write("") 
    
    st.info('This dashboard integrates NLP modules from Persons 1, 2, and 3.')
    st.warning('Ensure __init__.py is present in the modules folder.')
    
    # Large centered Orange/Yellow button
    analyze_btn = st.button('Analyze PR Health', type='primary')

# --- 4. INTEGRATION LOGIC ---
if analyze_btn:
    if not code_input.strip():
        st.error("Please provide code input first!")
    else:
        with st.spinner('Calculating health metrics...'):
            try:
                res_names = analyze_names(code_input)
                res_comments = analyze_comments(code_input)
                res_commit = score_commit(commit_input)
                rev_list = [r for r in reviews_input.split('\n') if r.strip()]
                res_sentiment = analyze_sentiment(rev_list)
                
                results = [res_names, res_comments, res_commit, res_sentiment]

                st.divider()
                st.header('Analysis Results')

                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                m_col1.metric("Name Quality", f"{res_names['score']}%")
                m_col2.metric("Comment Quality", f"{res_comments['score']}%")
                m_col3.metric("Commit Score", f"{res_commit['score']}%")
                m_col4.metric("Sentiment", f"{res_sentiment['score']}%")

                avg_score = round(sum(r['score'] for r in results) / 4)
                st.progress(avg_score / 100)
                st.subheader(f"Overall Health: {avg_score}%")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("Flags 🚩")
                    for r in results:
                        for flag in r.get('flags', []):
                            st.warning(f"**{r['module'].upper()}**: {flag}")
                with c2:
                    st.subheader("Suggestions 💡")
                    for r in results:
                        for sug in r.get('suggestions', []):
                            st.info(f"**{r['module'].upper()}**: {sug}")
            except Exception as e:
                st.error(f"Analysis failed: {e}")