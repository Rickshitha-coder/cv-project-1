import streamlit as st
from PIL import Image
import numpy as np
import cv2

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Color ↔ B&W Converter", layout="wide")
st.title("🎨 Color ↔ Black & White Converter")

# Choose mode
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
st.subheader("2️⃣ Upload Image")
uploaded_file = st.file_uploader("Upload Image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_np = np.array(img)

    if mode == "Black & White":
        # Convert to grayscale
        if len(img_np.shape) == 3 and img_np.shape[2] == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        st.image(gray, caption="Black & White Image", channels="GRAY")
    else:
        st.image(img_np, caption="Color Image", channels="RGB")
