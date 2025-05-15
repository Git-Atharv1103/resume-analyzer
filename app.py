import streamlit as st
import PyPDF2
from utils import extract_skills, load_job_descriptions, recommend_jobs
from streamlit_lottie import st_lottie
import requests
import time

# Page config
st.set_page_config(
    page_title="🌈 AI Resume Analyzer - Fun & Interactive",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Lottie animation from URL safely
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except:
        return None

# Load animations
resume_anim = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_u4yrau.json")
job_anim = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_ydo1amjm.json")
skill_anim = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_yt7vcnoc.json")

# Custom CSS for gradients and shadows
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .title {
        font-size: 3.5rem;
        font-weight: 900;
        text-shadow: 3px 3px 5px #000000aa;
    }
    .subtitle {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 25px;
    }
    .skill-bar {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        margin-bottom: 15px;
        overflow: hidden;
    }
    .skill-progress {
        background: #ffd166;
        height: 25px;
        border-radius: 15px;
        line-height: 25px;
        color: #333;
        font-weight: bold;
        text-align: center;
        transition: width 1.5s ease-in-out;
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 0.9rem;
        opacity: 0.7;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Main container
with st.container():
    st.markdown('<h1 class="title">✨ AI-Powered Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload your resume and get smart job recommendations with style! 🚀</p>', unsafe_allow_html=True)

    # Animations and upload side by side
    col1, col2 = st.columns([2, 3])
    with col1:
        if resume_anim is not None:
            st_lottie(resume_anim, height=250)
        else:
            st.warning("Resume animation failed to load.")
    with col2:
        uploaded_file = st.file_uploader("📂 Upload Resume (PDF)", type=["pdf"], help="Try uploading your resume PDF file")

if uploaded_file:
    with st.spinner('Analyzing your resume... Please wait! ⏳'):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
        time.sleep(1.5)  # simulate loading

    # Show resume preview
    st.markdown("### 📋 Extracted Resume Content Preview")
    st.write(resume_text[:1200] + " ...")

    # Extract skills and animate skill bars
    skills = extract_skills(resume_text)
    st.markdown("### 🛠️ Extracted Skills")
    if skills:
        for skill in skills:
            st.markdown(f"""
                <div class="skill-bar">
                    <div class="skill-progress" style="width: 90%;">{skill.capitalize()}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No matching skills found. Try uploading a different resume.")

    # Load jobs and show animation
    job_df = load_job_descriptions("job_descriptions.csv")
    recommended_jobs = recommend_jobs(resume_text, job_df)

    st.markdown("### 🎯 Recommended Jobs For You")
    col3, col4 = st.columns([3, 1])
    with col3:
        st.table(recommended_jobs.style.format({'Similarity_Score': '{:.2f}'}))
    with col4:
        if job_anim is not None:
            st_lottie(job_anim, height=150)
        else:
            st.warning("Job animation failed to load.")

    # Skill Gap Analysis
    ideal_skills = {'machine learning', 'python', 'data visualization', 'cloud computing'}
    missing_skills = ideal_skills - set(skills)
    st.markdown("### 🔎 Skill Gap Analysis")
    if missing_skills:
        st.error(f"Improve these skills to boost your profile: {', '.join(missing_skills)}")
    else:
        st.success("You're rocking! Your skills match top job profiles!")

else:
    st.info("👆 Please upload your resume PDF to start analysis.")

st.markdown('<div class="footer">Developed with ❤️ by Atharv — Enjoy your job hunt!</div>', unsafe_allow_html=True)
