# parking_slot_detection_streamlit.py

import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Parking Slot Detection", layout="wide")
st.title("🅿️ Parking Slot Detection Demo")

# Load the uploaded image
img_path = "/mnt/data/fb8aad3b-eaf3-43d3-b070-eec014158ce5.png"
img = cv2.imread(img_path)
original_img = img.copy()

st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Parking Lot Image", use_column_width=True)

# --------------------------
# Step 1: Define Parking Slots
# (x, y, width, height) manually for your uploaded image
parking_slots = [
    (0, 0, 140, 200),    # Top-left
    (150, 0, 140, 200),
    (300, 0, 140, 200),
    (450, 0, 140, 200),
    (0, 200, 140, 200),  # Bottom row
    (150, 200, 140, 200),
    (300, 200, 140, 200),
    (450, 200, 140, 200)
]

# --------------------------
# Step 2: Detect Occupancy
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

# --------------------------
st.write(f"### Available Slots: {free_count} / {len(parking_slots)}")
st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Parking Slot Detection Result", use_column_width=True)
