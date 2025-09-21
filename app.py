import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="ResuMatch - Resume Relevance Checker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Custom CSS for Professional UI
# ---------------------------
st.markdown("""
    <style>
    /* Page background and font */
    .reportview-container {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Form section */
    .stForm {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }

    /* Input labels */
    label {
        font-weight: bold;
        color: #495057;
    }

    /* File uploader */
    div.stFileUploader {
        border: 2px dashed #0a6ebd;
        border-radius: 8px;
        padding: 15px;
        background-color: #e9f2fb;
    }

    /* Submit button */
    div.stButton > button {
        background-color: #0a6ebd;
        color: white;
        font-weight: bold;
        padding: 0.5em 1.2em;
        border-radius: 8px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #0857a6;
        color: white;
    }

    /* Result card */
    .result-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }

    /* Metric style */
    .metric-label {
        font-weight: 600;
        font-size: 16px;
        color: #495057;
    }
    .metric-value {
        font-size: 32px;
        color: #0a6ebd;
        font-weight: bold;
    }

    /* Verdict text */
    .verdict-high { color: #28a745; font-weight:bold; font-size:18px; }
    .verdict-medium { color: #ffc107; font-weight:bold; font-size:18px; }
    .verdict-low { color: #dc3545; font-weight:bold; font-size:18px; }

    /* DataFrame container */
    .dataframe-container {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Page Header
# ---------------------------
st.title("ResuMatch – Resume Relevance Checker")
st.markdown("Upload resumes and job descriptions to check relevance score, missing skills, and suitability.")

# ---------------------------
# Resume Analysis Form
# ---------------------------
st.subheader("Resume Analysis")
with st.form("upload_form"):
    candidate = st.text_input("Candidate Name")
    job_id = st.text_input("Job ID")
    resume = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    jd = st.file_uploader("Upload Job Description (TXT/PDF)", type=["txt", "pdf"])
    submitted = st.form_submit_button("Analyze Resume")

    if submitted:
        if not candidate or not job_id or not resume or not jd:
            st.error("Please provide all required inputs.")
        else:
            files = {"resume": resume, "jd": jd}
            data = {"job_id": job_id, "candidate": candidate}
            response = requests.post(f"{BACKEND_URL}/analyze", files=files, data=data)

            if response.status_code == 200:
                result = response.json()
                
                # Result card
                
                st.markdown(f"**Candidate:** {result['candidate']}")
                
                # Relevance Score
                st.markdown(f"<div class='metric-label'>Relevance Score</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{result['score']:.2f} / 100</div>", unsafe_allow_html=True)
                st.progress(result['score'] / 100)
                
                # Verdict
                verdict_class = "verdict-high" if result["verdict"]=="High" else "verdict-medium" if result["verdict"]=="Medium" else "verdict-low"
                st.markdown(f"<p class='{verdict_class}'>Verdict: {result['verdict']}</p>", unsafe_allow_html=True)
                
                # Missing Keywords
                st.markdown("**Missing Keywords/Skills:**")
                if result["missing"]:
                    st.write(", ".join(result["missing"]))
                else:
                    st.write("No major gaps detected.")
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Failed to analyze resume. Please try again.")

# ---------------------------
# Results Dashboard
# ---------------------------
st.subheader("Results Dashboard")
job_id_query = st.text_input("Enter Job ID to fetch results")
if st.button("Get Results"):
    if not job_id_query:
        st.error("Please enter a Job ID.")
    else:
        response = requests.get(f"{BACKEND_URL}/results/{job_id_query}")
        if response.status_code == 200:
            results = response.json()
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No results found for this Job ID.")
        else:
            st.error("Failed to fetch results. Please try again.")
