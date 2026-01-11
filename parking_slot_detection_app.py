import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Parking Slot Detection", layout="wide")
st.title("🅿️ Parking Slot Detection Demo")

# --------------------------
# Upload an image
uploaded_file = st.file_uploader("Upload a parking lot image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Convert uploaded file to OpenCV image
    image = Image.open(uploaded_file)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    original_img = img.copy()

    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Parking Lot Image", use_column_width=True)

    # --------------------------
    # Define Parking Slots (adjust manually based on your image)
    # Here, I’m using 8 slots as in your previous code
    parking_slots = [
        (0, 0, 140, 200),
        (150, 0, 140, 200),
        (300, 0, 140, 200),
        (450, 0, 140, 200),
        (0, 200, 140, 200),
        (150, 200, 140, 200),
        (300, 200, 140, 200),
        (450, 200, 140, 200)
    ]

    # --------------------------
    # Detect occupancy
    free_count = 0
    for (x, y, w, h) in parking_slots:
        slot_img = img[y:y+h, x:x+w]
        gray = cv2.cvtColor(slot_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 1)
        thresh = cv2.adaptiveThreshold(
            blur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 25, 16
        )
        non_zero_count = cv2.countNonZero(thresh)

        # Simple threshold for occupancy (tune as needed)
        if non_zero_count > 5000:
            color = (0, 0, 255)  # Red → OCCUPIED
            status = "OCCUPIED"
        else:
            color = (0, 255, 0)  # Green → FREE
            status = "FREE"
            free_count += 1

        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
        cv2.putText(img, status, (x+5, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    st.write(f"### Available Slots: {free_count} / {len(parking_slots)}")
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Parking Slot Detection Result", use_column_width=True)
else:
    st.info("Please upload a parking lot image to start detection.")
