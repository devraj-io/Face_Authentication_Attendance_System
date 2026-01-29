import cv2
import face_recognition
import numpy as np
import csv
import pickle
import os
from datetime import datetime

video_capture = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []

if os.path.exists('encodings.pkl'):
    with open('encodings.pkl', 'rb') as f:
        data = pickle.load(f)
        known_face_encodings = data['encodings']
        known_face_names = data['names']

def log_attendance(name, status):
    with open('attendance.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        now = datetime.now()
        dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([name, dt_string, status])

print("Press 'r' to Register, 'q' to Quit, 'p' for Punch-in, 'o' for Punch-out")

while True:
    ret, frame = video_capture.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Face Attendance System', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):
        name = input("Enter name to register: ")
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(name)
            with open('encodings.pkl', 'wb') as f:
                pickle.dump({'encodings': known_face_encodings, 'names': known_face_names}, f)
            print(f"Registered {name}")

    elif key == ord('p') and name != "Unknown":
        log_attendance(name, "Punch-in")
        print(f"Punched-in: {name}")
    elif key == ord('o') and name != "Unknown":
        log_attendance(name, "Punch-out")
        print(f"Punched-out: {name}")
    elif key == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
