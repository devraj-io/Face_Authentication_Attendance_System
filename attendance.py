import cv2
import face_recognition
import pickle
import os
from datetime import datetime


known_encodings = []
known_names = []

if not os.path.exists('faces'):
    print("Error: No 'faces' folder found. Please run register.py first.")
    exit()

for file in os.listdir('faces'):
    if file.endswith('.pkl'):
        with open(f"faces/{file}", "rb") as f:
            data = pickle.load(f)
            known_encodings.append(data["encoding"])
            known_names.append(data["name"])

cap = cv2.VideoCapture(0)

print("System Active.")
print("Press 'p' to Punch-in | Press 'o' to Punch-out | Press 'q' to Quit")

while True:
    ret, frame = cap.read()
    if not ret: break

    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    current_name = "Unknown"

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        
        if True in matches:
            first_match_index = matches.index(True)
            current_name = known_names[first_match_index]

        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, current_name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Attendance System", frame)
    
   
    key = cv2.waitKey(1) & 0xFF

    if current_name != "Unknown":
        if key == ord('p') or key == ord('P'):
            
            with open("attendance_log.csv", "a") as f:
                f.write(f"{current_name},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},Punch-in\n")
            print(f"Punched-in: {current_name}")
            
        elif key == ord('o') or key == ord('O'):
            
            with open("attendance_log.csv", "a") as f:
                f.write(f"{current_name},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},Punch-out\n")
            print(f"Punched-out: {current_name}")

    if key == ord('q') or key == ord('Q'):
        break

cap.release()
cv2.destroyAllWindows()