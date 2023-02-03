import streamlit as st 
import PyPDF2
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))

st.title("Resume Screening Portal")

st.subheader("NLP Based Resume Screening")

st.caption("Aim of this project is to check whether a candidate is qualified for a role based his or her education, experience, and other information captured on their resume. In a nutshell, it's a form of pattern matching between a job's requirements and the qualifications of a candidate based on their resume.")

uploadedJD = st.file_uploader("Upload Job Description", type="pdf")

JD = st.text_area("Enter the job description: ")

uploadedResume = st.file_uploader("Upload resume",type="pdf")

click = st.button("Process")



try:
    global job_description
    with pdfplumber.open(uploadedJD) as pdf:
      for page in pdf.pages:
        job_description = ""
        job_description += page.extract_text()
      words = word_tokenize(job_description)
      job_description = [word for word in words if word.lower() not in stop_words]
      job_description = " ".join(job_description)        
except:
    st.write("")
    
    
try:
    global resume
    with  pdfplumber.open(uploadedResume) as pdf:
      for page in pdf.pages:
        resume = ""
        resume += page.extract_text()
      words = word_tokenize(resume)
      resume = [word for word in words if word.lower() not in stop_words]
      resume = " ".join(resume)
except:
    st.write("")
    
#logic
def getResult(JD_txt,resume_txt):
    content = [JD_txt, resume_txt]

    cv = CountVectorizer()

    matrix = cv.fit_transform(content)

    similarity_matrix =  cosine_similarity(matrix)

    match = similarity_matrix[0][1] * 100

    return match


#button 


if click:
  if JD == "":
    match = getResult(job_description, resume)
    match = round(match,2)
    st.write("Match Percentage: ",match,"%")
  else:
    match = getResult(JD, resume)
    match =  round(match,2)
    st.write("Match Percentage: ",match,"%")


st.caption(" ~ made by Jay Bhatt")