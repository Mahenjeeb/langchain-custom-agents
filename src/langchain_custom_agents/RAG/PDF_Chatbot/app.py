import os, streamlit as st
from pathlib import Path

pdf_source_path = Path(__file__).parent / "pdfs"
uploaded_file = st.file_uploader("Upload File", type="pdf")
if uploaded_file is not None:
    if (uploaded_file.name in os.listdir(pdf_source_path)):
        st.error("PDF Exists, Please upload a new PDF file")
    else: 
        file_path = os.path.join(pdf_source_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            st.success(f"File saved successfully to: {file_path}")