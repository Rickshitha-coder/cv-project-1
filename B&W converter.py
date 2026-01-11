import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from docx import Document
import fitz  # PyMuPDF
from PyPDF2 import PdfWriter, PdfReader

# -------------------------------
# Streamlit Page Config
# -------------------------------
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
    else:
        st.error("Could not access webcam.")

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
        if img is None:
            st.error("Could not read image file.")
        else:
            if mode == "Black & White":
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                st.image(gray, caption="Black & White Image", channels="GRAY")
            else:
                st.image(img, caption="Color Image", channels="BGR")
    
    # ---------- PDF Files ----------
    elif uploaded_file.type == "application/pdf":
        try:
            doc = fitz.open(stream=BytesIO(file_bytes), filetype="pdf")
            st.write(f"PDF has {doc.page_count} pages.")
            converted_pages = []

            for i, page in enumerate(doc):
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                if mode == "Black & White":
                    img = img.convert("L")  # grayscale
                converted_pages.append(img)
                st.image(img, caption=f"Page {i+1}")

            # Save as new PDF for download
            pdf_bytes = BytesIO()
            converted_pages[0].save(pdf_bytes, format="PDF", save_all=True, append_images=converted_pages[1:])
            st.download_button("Download Converted PDF", pdf_bytes.getvalue(), file_name="converted.pdf")
        except Exception as e:
            st.error(f"Failed to process PDF: {e}")
    
    # ---------- Word Files ----------
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        st.warning("Word image extraction is not fully supported. "
                   "Please convert Word to PDF first for full functionality.")
