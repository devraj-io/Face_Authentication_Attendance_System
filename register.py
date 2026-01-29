import cv2
import face_recognition
import pickle
import os


if not os.path.exists('faces'):
    os.makedirs('faces')

def register_user(name):
   
    cap = cv2.VideoCapture(0)
    print(f"--- Registering: {name} ---")
    print("1. Center your face in the box.")
    print("2. Press 'S' to save and register.")
    print("3. Press 'Q' to cancel.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break


        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
       
        face_locations = face_recognition.face_locations(rgb_frame)

       
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (left, top - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

      
        cv2.imshow("Registration - Center Your Face", frame)
        
      
        key = cv2.waitKey(1) & 0xFF
        
     
        if key == ord('s') or key == ord('S'):
            if len(face_locations) > 0:
                
                encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                
               
                data = {"name": name, "encoding": encoding}
                with open(f"faces/{name}.pkl", "wb") as f:
                    pickle.dump(data, f)
                
                print(f"Successfully registered {name}!")
                break
            else:
                print("Error: No face detected. Please try again.")

       
        elif key == ord('q') or key == ord('Q'):
            print("Registration cancelled.")
            break
    
    cap.release()
    cv2.destroyAllWindows()


user_name = input("Enter name for registration: ")
register_user(user_name)