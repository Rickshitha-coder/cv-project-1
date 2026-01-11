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

# Using Streamlit camera_input for webcam
webcam_img = st.camera_input("Take a Webcam Snapshot")

if webcam_img is not None:
    img = Image.open(webcam_img)
    img_np = np.array(img)

    if mode == "Black & White":
        if len(img_np.shape) == 3 and img_np.shape[2] == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        st.image(gray, caption="Black & White Snapshot", channels="GRAY")
        # Prepare download
        download_img = Image.fromarray(gray)
    else:
        st.image(img_np, caption="Color Snapshot", channels="RGB")
        download_img = img

    # Download button
    buf = BytesIO()
    download_img.save(buf, format="PNG")
    st.download_button(
        "⬇️ Download Image",
        data=buf.getvalue(),
        file_name="snapshot.png",
        mime="image/png"
    )

st.write("---")
st.subheader("2️⃣ Upload Image (JPG/PNG)")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_np = np.array(img)

    if mode == "Black & White":
        if len(img_np.shape) == 3 and img_np.shape[2] == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        st.image(gray, caption="Black & White Image", channels="GRAY")
        download_img = Image.fromarray(gray)
    else:
        st.image(img_np, caption="Color Image", channels="RGB")
        download_img = img

    # Download button
    buf = BytesIO()
    download_img.save(buf, format="PNG")
    st.download_button(
        "⬇️ Download Image",
        data=buf.getvalue(),
        file_name="converted_image.png",
        mime="image/png"
    )
