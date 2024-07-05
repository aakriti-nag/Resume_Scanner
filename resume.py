from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf(upload_file):
    if upload_file is not None:
        images = pdf2image.convert_from_bytes(upload_file.read())
        first_page = images[0]
        image_byte_arr = io.BytesIO()
        first_page.save(image_byte_arr, format='JPEG')
        image_byte_arr = image_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": 'image/jpeg',
                'data': base64.b64encode(image_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title='Resume Checker', layout='wide')
st.sidebar.header("Navigation")
st.sidebar.write("Use the main panel to upload your resume and get the evaluation.")
st.sidebar.write("[Learn more about resume optimization](https://www.example.com)")

col1, col2 = st.columns([2, 1])

with col1:
    st.header('Resume Checking Application')
    input_text = st.text_area("Enter the Job Description:", key='input')
    upload_file = st.file_uploader("Upload Resume...", type=['pdf'])

with col2:
    st.write(' ')
    st.write(' ')
    if upload_file is not None:
        st.success('Resume Uploaded Successfully')
        st.write('Choose from the below common questions')

    submit1 = st.button("Tell me about the Resume", help="Get a detailed evaluation of your resume based on the job description")
    submit2 = st.button("Percentage match", help="Find out the percentage match of your resume with the job description")

input_prompt1 = """
 You are an experienced technical hiring manager in the field of any one job role data science or data analyst or big data engineer or machine learning.
 Your task is to review the given resume against the job description for these roles. Check their experience and projects.
 Please share your professional evaluation on whether the candidate's profile aligns with the role or not. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
 And what the candidiate can do to improve their chances in order to land in the role.
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science or data analysis or big data engineer or machine learning.
Your task is to evaluate the resume against the provided job description focusing mainly on the job requirements from the experience and project of the resume. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and that needs to be added and last final thoughts.
"""

with st.expander("Instructions"):
    st.write("""
        1. Enter the job description in the text area.
        2. Upload your resume in PDF format.
    """)

if submit1 or submit2:
    with st.spinner('Processing...'):
        if upload_file is not None:
            pdf_content = input_pdf(upload_file)
            response = get_response(input_prompt1 if submit1 else input_prompt2, pdf_content, input_text)
            st.success("Processing Complete")
            st.subheader("Output: ")
            st.markdown(response.replace("\n", "\n\n"))
        else:
            st.warning("Please upload a resume to proceed")
