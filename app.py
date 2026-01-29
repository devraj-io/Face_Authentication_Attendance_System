from flask import Flask, render_template, Response, request, redirect
import cv2
import face_recognition
import pickle
import os
from datetime import datetime

app = Flask(__name__)
camera = cv2.VideoCapture(0)


known_encodings = []
known_names = []
if os.path.exists('faces'):
    for file in os.listdir('faces'):
        with open(f"faces/{file}", "rb") as f:
            data = pickle.load(f)
            known_encodings.append(data["encoding"])
            known_names.append(data["name"])

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
                name = "Unknown"
                matches = face_recognition.compare_faces(known_encodings, encoding)
                if True in matches:
                    name = known_names[matches.index(True)]

                
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/punch', methods=['POST'])
def punch():
    action = request.form.get('action') 
    success, frame = camera.read()
    if success:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_frame)
        if face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encodings[0])
            if True in matches:
                name = known_names[matches.index(True)]
                with open("attendance_log.csv", "a") as f:
                    f.write(f"{name},{datetime.now()},{action}\n")
                return f"<h1>Success! {name} {action}ed.</h1><a href='/'>Back</a>"
    return "<h1>Error: Face not recognized.</h1><a href='/'>Try Again</a>"

if __name__ == '__main__':
    app.run(debug=True)