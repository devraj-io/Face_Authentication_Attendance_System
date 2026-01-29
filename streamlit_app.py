import streamlit as st
import face_recognition
import pickle
import os
from datetime import datetime
import numpy as np

# Ensure project structure for deliverables [cite: 16, 17]
FACES_DIR = 'faces'
if not os.path.exists(FACES_DIR):
    os.makedirs(FACES_DIR)

st.set_page_config(page_title="AI Attendance System", layout="wide")

st.title("Face Authentication Attendance System")
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Signup (Register)", "Login (Attendance)"])

# Load known faces from the 'faces' folder
def load_known_faces():
    known_encodings = []
    known_names = []
    for file in os.listdir(FACES_DIR):
        if file.endswith('.pkl'):
            with open(os.path.join(FACES_DIR, file), "rb") as f:
                data = pickle.load(f)
                known_encodings.append(data["encoding"])
                known_names.append(data["name"])
    return known_encodings, known_names

if choice == "Signup (Register)":
    st.subheader("User Registration")
    st.info("Your face will be converted to a 128D encoding and stored for future matching.")
    
    name = st.text_input("Enter Full Name")
    # Real camera input requirement [cite: 12]
    img_file = st.camera_input("Capture Face for Signup")
    
    if img_file and name:
        # Load the uploaded image
        image = face_recognition.load_image_file(img_file)
        # Identify the face and generate encoding 
        encodings = face_recognition.face_encodings(image)
        
        if encodings:
            # Save ONLY the encoding, not the raw image, for efficiency and privacy
            encoding_data = {"name": name, "encoding": encodings[0]}
            with open(os.path.join(FACES_DIR, f"{name}.pkl"), "wb") as f:
                pickle.dump(encoding_data, f)
            st.success(f"Successfully registered {name}!")
        else:
            st.error("No face detected. Please try again with better lighting.")

elif choice == "Login (Attendance)":
    st.subheader("Mark Your Attendance")
    known_encodings, known_names = load_known_faces()
    
    # Capture live frame for identification 
    login_img = st.camera_input("Look at the camera to verify")
    
    if login_img:
        # The capture is processed in memory but NOT stored in the 'faces' folder
        test_image = face_recognition.load_image_file(login_img)
        test_encodings = face_recognition.face_encodings(test_image)
        
        if test_encodings:
            current_encoding = test_encodings[0]
            # Compare live capture against stored face encodings
            matches = face_recognition.compare_faces(known_encodings, current_encoding)
            
            if True in matches:
                match_index = matches.index(True)
                identified_name = known_names[match_index]
                
                st.success(f"Identity Verified: **{identified_name}**")
                
                # Logic for Punch-in and Punch-out [cite: 9, 11]
                col1, col2 = st.columns(2)
                
                if col1.button(f"Punch-in as {identified_name}"):
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    with open("attendance_log.csv", "a") as f:
                        f.write(f"{identified_name},{timestamp},Punch-in\n")
                    st.balloons()
                    st.info(f"Punched-in: {identified_name} at {timestamp}")
                
                if col2.button(f"Punch-out as {identified_name}"):
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    with open("attendance_log.csv", "a") as f:
                        f.write(f"{identified_name},{timestamp},Punch-out\n")
                    st.warning(f"Punched-out: {identified_name} at {timestamp}")
            else:
                st.error("Face not recognized. Please register first.")
        else:
            st.error("Face detection failed. Ensure you are facing the camera.")