
Face Authentication Attendance System

A robust, real-time face recognition application built with Streamlit, OpenCV, and Dlib to automate attendance tracking. This project was developed as part of an AI/ML Intern Assignment.

🚀 Features



Face Registration: Capture and store 128D facial encodings for new users.



Real-time Identification: Matches live camera feed against the database without storing temporary images.



Attendance Logging: Specific buttons for Punch-in and Punch-out with precise timestamps.



Robust Pre-processing: Handles varying lighting conditions using Histogram Equalization.



Spoof Prevention: Basic liveness detection check to ensure a physical presence.

🛠️ Technical Approach



Face Detection: Uses HOG (Histogram of Oriented Gradients) to locate faces in real-time.



Feature Extraction: Utilizes a pre-trained ResNet-34 network from the dlib library to generate a 128D vector representing facial features.



Matching Logic: Employs Euclidean Distance comparison; a distance of $< 0.6$ confirms an identity match.

Database: Stores user data in lightweight .pkl files, ensuring privacy by not saving actual photos of the users.

📈 Accuracy & Performance



Model Benchmark: The underlying model achieves 99.38% accuracy on the LFW (Labeled Faces in the Wild) dataset.



Latency: Average recognition time is $< 0.5$ seconds on standard CPU hardware.

⚠️ Known Failure Cases



Extreme Profiles: Accuracy decreases if the head is tilted more than 45 degrees.



Heavy Occlusions: Sunglasses, large masks, or hair covering the eyes may prevent landmark detection.



Low Light: Performance is limited in environments where the sensor cannot distinguish facial contrast.

📂 Project Structure

Plaintext



├── faces/               # Local database of registered face encodings (.pkl)

├── streamlit_app.py     # Main application logic

├── attendance_log.csv   # Log file for Punch-in/out records

├── requirements.txt     # List of dependencies

└── README.md            # Project documentation

⚙️ Installation & Usage

Clone the Repository:

Bash
```
git clone https://github.com/devraj-io/Face_Authentication_Attendance_System.gitcd Face_Authentication_Attendance_System
```
Install Dependencies:
```
pip install -r requirements.txt
```
Run the App:
```
streamlit run streamlit_app.py
```
