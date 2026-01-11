import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from docx import Document
from pdf2image import convert_from_bytes
from PyPDF2 import PdfWriter, PdfReader

st.set_page_config(page_title="Universal Color ↔ B&W Converter", layout="wide")
st.title("🎨 Universal Color ↔ Black & White Converter")

mode = st.radio("Choose Mode:", ("Color", "Black & White"))

st.write("---")
st.subheader("1️⃣ Webcam Snapshot")
if st.button("Take Webcam Snapshot"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        if mode == "Black & White":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            st.image(frame, caption="Black & White Snapshot", channels="GRAY")
        else:
            st.image(frame, caption="Color Snapshot", channels="BGR")

st.write("---")
st.subheader("2️⃣ Upload Image or Document")
uploaded_file = st.file_uploader(
    "Upload Image (JPG, PNG) or Document (PDF, DOCX)", 
    type=["jpg", "jpeg", "png", "pdf", "docx"]
)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    # ---------- Image Files ----------
    if uploaded_file.type in ["image/jpeg", "image/png"]:
        img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        if mode == "Black & White":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            st.image(gray, caption="Black & White Image", channels="GRAY")
        else:
            st.image(img, caption="Color Image", channels="BGR")

    # ---------- PDF Files ----------
    elif uploaded_file.type == "application/pdf":
        images = convert_from_bytes(file_bytes)
        st.write(f"PDF has {len(images)} pages.")
        converted_pages = []
        for i, img in enumerate(images):
            img_np = np.array(img)
            if mode == "Black & White":
                gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
                converted_pages.append(Image.fromarray(gray))
            else:
                converted_pages.append(img)
            st.image(converted_pages[-1], caption=f"Page {i+1}")
        # Optional: Save as new PDF
        pdf_bytes = BytesIO()
        converted_pages[0].save(pdf_bytes, format="PDF", save_all=True, append_images=converted_pages[1:])
        st.download_button("Download Converted PDF", pdf_bytes.getvalue(), file_name="converted.pdf")

    # ---------- Word Files ----------
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(BytesIO(file_bytes))
        st.write(f"Word document has {len(doc.inline_shapes)} images.")
        # Extract images and convert
        for i, shape in enumerate(doc.inline_shapes):
            img = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
            st.write("Image conversion for Word inline shapes will require extra low-level handling.")
        st.info("PDF conversion is recommended for full document image extraction.")
