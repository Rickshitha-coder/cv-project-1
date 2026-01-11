import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# ----------------- Streamlit Page Setup -----------------
st.set_page_config(page_title="Color to B&W Converter", layout="wide")
st.title("🎨 Color ↔ Black & White Real-Time Converter")

# ----------------- Mode Selection -----------------
mode = st.radio("Choose Mode:", ("Color", "Black & White"))

# ----------------- Video Transformer -----------------
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")  # Get BGR frame
        if mode == "Black & White":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # Back to 3-channel for display
        return img

# ----------------- Start Webcam Stream -----------------
webrtc_streamer(
    key="color_bw_converter",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
)

# ----------------- Optional: Image Upload -----------------
st.write("---")
st.subheader("Or Upload an Image")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if mode == "Black & White":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        st.image(gray, caption="Black & White Image", channels="GRAY")
    else:
        st.image(img, caption="Color Image", channels="BGR")
