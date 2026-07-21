import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from docx import Document


# ======================
# Gemini API Key
# ======================
# Set API KEY

API_KEY = "AQ.Ab8RN6Lf35Ykj2DxbiAYk4VZ5tjwIPuCYh4Sl3gA5x2o4NBeow"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-3.5-flash"
)
# ======================
# Extract Resume Text  
# ======================

# pdf first
def extract_pdf(file):
    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        extracted =page.extract_text()
        if extracted:
            text += extracted
    return text

#docx second
def extract_docx(file):
    doc = Document(file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

# ======================
# ATS ANALSIS  
# ======================

def analyze_resume(resume_text, job_description):
    prompt =  f"""
        You are an experienced HR Recruiter and ATS specialist.
        Evaluate the candidate's resume against the job description.

        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Provide:
        
        1. ATS Match Score (0=100)
        2. Candidate Summary
        3. Strengths
        4. Weaknesses
        5. Missing Skills
        6. Recommend Improvements
        7. Interview Recomendation
            - Highly Recommended
            - Consider
            - Not Recommended
        8. Final Hiring Decision

        use professional recruiter language.
        """

    response = model.generate_content(
        prompt)
    
    
    return response.text  

# ======================
# UI INTERFACE  
# ======================


st.set_page_config(
    page_title="AI ATS Resume Analyser",
    layout="centered",
)


st.title("AI ATS Resume Scanner")
st.write(" Upload a candidate's resume and the job description to analyze the match.")
st.image("https://www.cloudapper.ai/wp-content/uploads/2025/08/AI-Resumes-Screening.png", width=600)


uploaded_file = st.file_uploader("Upload Resume here",
                               type=["pdf", "docx"])
 
job_description = st.text_area("Paste your job description here",
                                 height=200)

if st.button("Analyze Resume"):
    if uploaded_file is None:
        st.warning("Please upload a resume first")
    elif not job_description:
        st.warning("Please provide a job description")

    else:

        with st.spinner("Analyzing Resume....."):
            filename = uploaded_file.name.lower()
            if filename.endswith(".pdf"):
                resume_text = extract_pdf(uploaded_file)

            elif filename.endswith(".docx"):
                resume_text = extract_docx(uploaded_file)
            else:
                st.error("Unsupported File Format. Please upload a PDF or Docx File.") 

                st.stop()
            result = analyze_resume(resume_text, job_description)

            st.subheader("Analysis Completed!")
            st.markdown(result) 
