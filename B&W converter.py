import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="🎨 Color ↔ Black & White Converter",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
h1 {color: #4B0082; font-size: 2.5rem;}
h2 {color: #6A0DAD; font-size: 1.8rem;}
.stButton>button {background-color: #6A0DAD; color: white; border-radius: 10px; height: 3em;}
.stDownloadButton>button {background-color: #4B0082; color: white; border-radius: 10px; height: 3em;}
</style>
""", unsafe_allow_html=True)

st.title("🎨 Universal Color ↔ Black & White Converter")
st.markdown("Convert your images or webcam snapshots into **Color** or **Black & White** instantly!")

# -------------------------------
# Mode selection
# -------------------------------
mode = st.radio("Choose Mode:", ("Color", "Black & White"))

# -------------------------------
# Helper function: convert to B&W
# -------------------------------
def convert_to_bw(pil_img):
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")
    img_np = np.array(pil_img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    return Image.fromarray(gray)

# -------------------------------
# Webcam snapshot section
# -------------------------------
st.markdown("---")
st.subheader("1️⃣ Webcam Snapshot")

# Show camera widget
webcam_img = st.camera_input("Activate Webcam")

# Process snapshot only if button is clicked
if webcam_img is not None:
    if st.button("Take Snapshot"):
        img = Image.open(webcam_img)
        if mode == "Black & White":
            download_img = convert_to_bw(img)
            st.image(download_img, caption="Black & White Snapshot")
            filename = "webcam_snapshot_bw.png"
        else:
            download_img = img
            st.image(img, caption="Color Snapshot")
            filename = "webcam_snapshot_color.png"

        # Download button
        buf = BytesIO()
        download_img.save(buf, format="PNG")
        st.download_button(
            "⬇️ Download Snapshot",
            data=buf.getvalue(),
            file_name=filename,
            mime="image/png"
        )

# -------------------------------
# Image upload section
# -------------------------------
st.markdown("---")
st.subheader("2️⃣ Upload Image (JPG/PNG)")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    if mode == "Black & White":
        download_img = convert_to_bw(img)
        st.image(download_img, caption="Black & White Image")
        filename = "uploaded_image_bw.png"
    else:
        download_img = img
        st.image(img, caption="Color Image")
        filename = "uploaded_image_color.png"

    # Download button
    buf = BytesIO()
    download_img.save(buf, format="PNG")
    st.download_button(
        "⬇️ Download Converted Image",
        data=buf.getvalue(),
        file_name=filename,
        mime="image/png"
    )

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown(
    "<p style='color: gray; font-size:0.9rem;'>Developed with 💜 using Streamlit | Supports JPG & PNG images only | Webcam snapshot processed only when button clicked.</p>",
    unsafe_allow_html=True
)
