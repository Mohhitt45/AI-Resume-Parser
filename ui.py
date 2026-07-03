from pdf_generator import create_report
import streamlit as st
import requests

BASE_URL = "https://mohhitt45-ai-resume-parser.hf.space"


# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="AI Resume Intelligence System",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color: #F5F7FA;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.big-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #1E3A8A;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #6B7280;
    margin-bottom: 25px;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="big-title">
🚀 AI Resume Intelligence Platform
</div>

<div class="subtitle">
Semantic Resume Parsing • ATS Analysis • BERT Semantic Matching
</div>
""", unsafe_allow_html=True)

st.divider()

# ------------------------------
# Sidebar
# ------------------------------
with st.sidebar:
    st.header("About")
    st.write(
        """
        Upload a resume and paste a Job Description.

        The system will:

        ✅ Parse Resume

        ✅ Calculate ATS Score

        ✅ Perform BERT Semantic Matching

        ✅ Show Matched Skills

        ✅ Show Missing Skills
        """
    )

# ------------------------------
# Main Layout
# ------------------------------
left, right = st.columns([1,1])

with left:

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

with right:

    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

st.divider()

analyze = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

# ------------------------------
# API Call
# ------------------------------
if analyze:

    if uploaded_file is None:

        st.error("Please upload a resume.")
        st.stop()

    if job_description.strip() == "":

        st.error("Please enter Job Description.")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        data = {
            "job_description": job_description
        }

        response = requests.post(
            f"{BASE_URL}/match_resume_bert",
            files=files,
            data=data,
            timeout=60
        )

    if response.status_code != 200:

        st.error("API Error")
        st.stop()

    result = response.json()

    st.session_state["result"] = result

    # ============================================
# RESULTS DASHBOARD
# ============================================

if "result" in st.session_state and st.session_state["result"]:

    result = st.session_state["result"]

    st.divider()

    st.header("📊 Analysis Report")

    parsed = result["resume_data"]

    info = parsed.get("basic_info", {})

    ats = result["ats"]

    ats_score = ats.get("ats_score", 0)

    match_score = result.get("match_score", 0)

    col1, col2 = st.columns(2)

    # ATS SCORE
    with col1:

        st.markdown(f"""
        <div style="
            background:white;
            padding:25px;
            border-radius:15px;
            text-align:center;
            box-shadow:0px 3px 12px rgba(0,0,0,0.1);
        ">
            <h3>⭐ ATS Score</h3>
            <h1 style="color:#1E3A8A;">{ats_score}%</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div style="
            background:white;
            padding:25px;
            border-radius:15px;
            text-align:center;
            box-shadow:0px 3px 12px rgba(0,0,0,0.1);
        ">
            <h3>🎯 Job Match</h3>
            <h1 style="color:#16A34A;">{match_score}%</h1>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("👤 Candidate Information")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(f"**Name**\n\n{info.get("name", "N/A")}")

    with c2:
        st.info(f"**Email**\n\n{info.get("email", "N/A")}")

    with c3:
        st.info(f"**Phone**\n\n{info.get("phone", "N/A")}")

    st.divider()

    left, right = st.columns(2)

    # MATCHED SKILLS
    with left:

        st.subheader("✅ Matched Skills")

        matched = result.get("matched_skills", [])

        if len(matched) == 0:

            st.warning("No matched skills.")

        else:

            for skill in matched:

                st.success(skill)

    # MISSING SKILLS
    with right:

        st.subheader("❌ Missing Skills")

        missing = result.get("missing_skills", [])

        if len(missing) == 0:

            st.success("No missing skills.")

        else:

            for skill in missing:

                st.error(skill)

    st.divider()

    st.subheader("🛠 Extracted Skills")

    skills = parsed.get("skills", [])

    cols = st.columns(4)

    for i, skill in enumerate(skills):

        cols[i % 4].success(skill)

    st.divider()

    st.markdown("## 📊 AI Insights Dashboard")

    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg,#0F172A,#1E3A8A);
        padding:20px;
        border-radius:15px;
        color:white;
    ">
    <h4>🧠 AI Analysis Summary</h4>

    <p>✔ Resume analyzed using NLP + BERT embeddings</p>
    <p>✔ Semantic matching performed with Job Description</p>
    <p>✔ ATS score computed using weighted scoring model</p>

    </div>
    """, unsafe_allow_html=True)

if st.button("📄 Generate PDF Report"):

    file = create_report(result)

    with open(file, "rb") as pdf:

        st.download_button(
            "⬇ Download Report",
            pdf,
            file_name="Resume_Report.pdf",
            mime="application/pdf"
        )
st.markdown("""
<hr>

<div style="text-align:center; color:gray; padding:20px;">
🚀 Built with FastAPI • Streamlit • BERT • NLP • Python
</div>

""", unsafe_allow_html=True)       
