import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Color ↔ B&W Converter", layout="wide")
st.title("🎨 Color ↔ Black & White Converter")

mode = st.radio("Choose Mode:", ("Color", "Black & White"))

st.write("---")
st.subheader("1️⃣ Webcam Snapshot")

# -------------------------------
# Function to robustly convert to B&W
# -------------------------------
def convert_to_bw(pil_img):
    # Convert image to RGB first (handles grayscale, RGBA, palette images)
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")
    img_np = np.array(pil_img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    return Image.fromarray(gray)

# -------------------------------
# Webcam Input
# -------------------------------
webcam_img = st.camera_input("Take a Webcam Snapshot")

if webcam_img is not None:
    img = Image.open(webcam_img)
    if mode == "Black & White":
        download_img = convert_to_bw(img)
        st.image(download_img, caption="Black & White Snapshot")
    else:
        download_img = img
        st.image(img, caption="Color Snapshot")

    # Download button
    buf = BytesIO()
    download_img.save(buf, format="PNG")
    st.download_button(
        "⬇️ Download Snapshot",
        data=buf.getvalue(),
        file_name="webcam_snapshot.png",
        mime="image/png"
    )

st.write("---")
st.subheader("2️⃣ Upload Image (JPG/PNG)")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    if mode == "Black & White":
        download_img = convert_to_bw(img)
        st.image(download_img, caption="Black & White Image")
    else:
        download_img = img
        st.image(img, caption="Color Image")

    # Download button
    buf = BytesIO()
    download_img.save(buf, format="PNG")
    st.download_button(
        "⬇️ Download Converted Image",
        data=buf.getvalue(),
        file_name="converted_image.png",
        mime="image/png"
    )
