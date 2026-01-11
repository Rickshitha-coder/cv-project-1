import streamlit as st
from PIL import Image
from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader

st.set_page_config(page_title="Simple B&W Converter", layout="wide")
st.title("🎨 Image & Document Converter (B&W)")

mode = st.radio("Choose Mode:", ("Color", "Black & White"))

uploaded_file = st.file_uploader(
    "Upload Image (JPG, PNG) or Document (PDF, DOCX)",
    type=["jpg", "jpeg", "png", "pdf", "docx"]
)

if uploaded_file:
    file_bytes = uploaded_file.read()

    # Image handling
    if uploaded_file.type in ["image/jpeg", "image/png"]:
        img = Image.open(BytesIO(file_bytes))
        if mode == "Black & White":
            img = img.convert("L")
        st.image(img, caption="Converted Image")

    # PDF handling (metadata only)
    elif uploaded_file.type == "application/pdf":
        pdf = PdfReader(BytesIO(file_bytes))
        st.write(f"PDF has {len(pdf.pages)} pages. Rendering not supported in this build.")

    # Word handling
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(BytesIO(file_bytes))
        st.write(f"Word document has {len(doc.inline_shapes)} images (cannot render).")
