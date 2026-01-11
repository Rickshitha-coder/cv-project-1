import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="🎨 Color ↔ B&W Converter",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# CSS for professional look
# -------------------------------
st.markdown("""
<style>
/* Headings */
h1 {color: #4B0082; font-size: 2.8rem; font-weight:bold;}
h2 {color: #6A0DAD; font-size: 1.8rem; font-weight:bold;}

/* Section cards */
.section-card {
    padding: 20px;
    border-radius: 15px;
    background-color: #f7f7f7;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

/* Buttons */
.stButton>button {background-color: #6A0DAD; color: white; border-radius: 10px; height: 3em; font-weight:bold;}
.stDownloadButton>button {background-color: #4B0082; color: white; border-radius: 10px; height: 3em; font-weight:bold;}

/* Footer */
.footer {color: gray; font-size:0.9rem; text-align:center;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# App Title
# -------------------------------
st.title("🎨 Universal Color ↔ Black & White Converter")
st.markdown("Convert your images or webcam snapshots into **Color** or **Black & White** instantly!")

# -------------------------------
# Mode Selection
# -------------------------------
mode = st.radio("Choose Mode:", ("Color", "Black & White"), horizontal=True)

# -------------------------------
# Helper Function: Convert to B&W
# -------------------------------
def convert_to_bw(pil_img):
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")
    img_np = np.array(pil_img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    return Image.fromarray(gray)

# -------------------------------
# Webcam Section
# -------------------------------
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.subheader("📷 Webcam Snapshot")

# Session state for webcam
if "show_camera" not in st.session_state:
    st.session_state.show_camera = False

if st.button("Activate Webcam"):
    st.session_state.show_camera = True

if st.session_state.show_camera:
    webcam_img = st.camera_input("Take Snapshot")
    if webcam_img is not None:
        if st.button("Process Snapshot"):
            img = Image.open(webcam_img)
            if mode == "Black & White":
                download_img = convert_to_bw(img)
                st.image(download_img, caption="Black & White Snapshot")
                filename = "webcam_snapshot_bw.png"
            else:
                download_img = img
                st.image(img, caption="Color Snapshot")
                filename = "webcam_snapshot_color.png"

            # Download
            buf = BytesIO()
            download_img.save(buf, format="PNG")
            st.download_button(
                "⬇️ Download Snapshot",
                data=buf.getvalue(),
                file_name=filename,
                mime="image/png"
            )
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Upload Section
# -------------------------------
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.subheader("🖼️ Upload Image (JPG/PNG)")

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

    # Download
    buf = BytesIO()
    download_img.save(buf, format="PNG")
    st.download_button(
        "⬇️ Download Converted Image",
        data=buf.getvalue(),
        file_name=filename,
        mime="image/png"
    )
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown(
    "<p class='footer'>Developed with 💜 using Streamlit | Supports JPG & PNG images only | Webcam activates only after clicking 'Activate Webcam'.</p>",
    unsafe_allow_html=True
)
