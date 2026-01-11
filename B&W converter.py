import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Color to B&W Converter", layout="wide")
st.title("🎨 Color ↔ Black & White Converter")

mode = st.radio("Choose Mode:", ("Color", "Black & White"))

# Image Upload
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if mode == "Black & White":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        st.image(gray, caption="Black & White Image", channels="GRAY")
    else:
        st.image(img, caption="Color Image", channels="BGR")

# Webcam Snapshot
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
