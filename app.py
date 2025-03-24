# -*- coding: utf-8 -*-

import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import docx

st.set_page_config(page_title="LAVA Multi-Agent AI Assistant")
st.title("LAVA Multi-Agent AI Assistant")

st.markdown("""
Upload a topic or document and let our multi-agent AI system generate tailored marketing and communication content for both scientific and general audiences.
""")

# --- API Key Input ---
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# --- Topic or Document Input ---
topic = st.text_area("Enter a topic or brief description")
uploaded_file = st.file_uploader("Or upload a Word or PDF document", type=["pdf", "docx"])

# --- Extract text from uploaded document ---
def extract_text(file):
    if file.name.endswith(".pdf"):
        pdf = PdfReader(file)
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs if para.text])
    return ""

# --- Run agents ---
def call_agent(prompt):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if st.button("Run Multi-Agent AI") and api_key:
    input_text = topic or extract_text(uploaded_file)
    if not input_text:
        st.warning("Please provide a topic or upload a document.")
    else:
        with st.spinner("Running agents..."):
            agents = {
                "Scientific Blog Article": f"Write a short scientific article for our research blog at an expert reading level based on the following topic or text: {input_text}\nInclude a brief description of the article for our newsletter.",

                "General Blog Article": f"Write a short non-scientific article for our general audience blog at an 8th grade reading level based on the following topic or text: {input_text}\nInclude a brief and engaging description for our newsletter.",

                "General Social Media Posts": f"Create 5 engaging social media posts for a general audience based on the following topic or text: {input_text}",

                "Scientific Social Media Posts": f"Create 3 engaging social media posts for a scientific audience based on the following topic or text: {input_text}",

                "Video Script": f"Write a short explainer-style video script (1-2 minutes) for a general audience on the following topic or text: {input_text}",

                "FAQ Article": f"Create a Frequently Asked Questions article based on the following topic or text: {input_text}",

                "Fundraising Appeal Email": f"Write a fundraising appeal email for major philanthropic donors encouraging them to fund this important work based on the following topic or text: {input_text}"
            }

            for title, prompt in agents.items():
                st.subheader(title)
                result = call_agent(prompt)
                st.markdown(result)
