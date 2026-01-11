# Filename: parking_slot_detection_app.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Parking Slot Detection", layout="wide")

st.title("🅿️ Parking Slot Detection using OpenCV & Streamlit")

# Upload image
uploaded_file = st.file_uploader("Upload Parking Lot Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    original_img = img.copy()
    
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Parking Lot Image", use_column_width=True)

    st.write("### Step 1: Define Parking Slots (Manually in code)")

    # Define parking slot coordinates manually (x, y, w, h)
    # You can modify these coordinates for your image
    parking_slots = [
        (50, 100, 150, 80),
        (220, 100, 150, 80),
        (390, 100, 150, 80),
        (50, 200, 150, 80),
        (220, 200, 150, 80),
        (390, 200, 150, 80)
    ]

    st.write(f"Total Slots Defined: {len(parking_slots)}")

    st.write("### Step 2: Detect Occupancy")

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
        # print(non_zero_count)

        # Threshold for empty/occupied (tune this based on image)
        if non_zero_count > 900:
            color = (0, 0, 255)  # Red → OCCUPIED
            status = "OCCUPIED"
        else:
            color = (0, 255, 0)  # Green → FREE
            status = "FREE"
            free_count += 1

        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
        cv2.putText(img, status, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    st.write(f"### Available Slots: {free_count} / {len(parking_slots)}")

    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Parking Slot Detection Result", use_column_width=True)

else:
    st.info("Upload an image to start parking slot detection.")
