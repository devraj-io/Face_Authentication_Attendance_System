# Face Authentication Attendance System

A real-time **Face Authentication–based Attendance System** built using **Streamlit**, **OpenCV**, and **Dlib**.
The system automates attendance marking through facial recognition while ensuring privacy, efficiency, and robustness.
This project was developed as part of an **AI/ML Internship Assignment**.

---

## 🚀 Key Features

* **Face Registration**
  Registers new users by extracting and storing **128-dimensional facial embeddings** instead of raw images, ensuring data privacy.

* **Real-Time Face Authentication**
  Identifies users from a live camera feed by matching facial embeddings against the stored database.

* **Attendance Management**
  Separate **Punch-In** and **Punch-Out** actions with accurate timestamp logging in CSV format.

* **Image Pre-processing**
  Applies **Histogram Equalization** to improve robustness under varying lighting conditions.

* **Basic Spoof Prevention**
  Includes a simple **liveness check** to reduce spoofing attempts using static images.

---

## 🛠️ Technical Approach

### 1️⃣ Face Detection

* Implemented using **Histogram of Oriented Gradients (HOG)** for efficient and fast face localization on CPU-based systems.

### 2️⃣ Feature Extraction

* Uses **Dlib’s pre-trained ResNet-34 model** to extract **128D facial embeddings** that uniquely represent each individual.

### 3️⃣ Face Matching

* **Euclidean Distance** is used to compare embeddings.
* A configurable distance threshold determines identity matches.

### 4️⃣ Data Storage

* Facial embeddings are stored locally in lightweight **`.pkl` files**.
* No facial images are saved, preserving user privacy.

---

## 📈 Accuracy & Performance

* **Model Accuracy**
  The underlying Dlib face recognition model achieves **99.38% accuracy** on the **LFW (Labeled Faces in the Wild)** benchmark dataset.

* **Inference Speed**
  Average recognition latency is low and runs efficiently on standard CPU hardware without GPU acceleration.

---

## ⚠️ Known Failure Cases

* **Extreme Head Angles**
  Recognition accuracy decreases when the face is rotated beyond ~45°.

* **Occlusions**
  Sunglasses, face masks, or heavy hair obstruction may prevent accurate landmark detection.

* **Low-Light Conditions**
  Performance degrades when facial contrast is insufficient due to poor lighting.

---

## 📂 Project Structure

```text
├── faces/                 # Stored facial embeddings (.pkl files)
├── streamlit_app.py       # Main Streamlit application
├── attendance_log.csv     # Punch-in / Punch-out records
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Installation & Usage

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/devraj-io/Face_Authentication_Attendance_System.git
cd Face_Authentication_Attendance_System
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
streamlit run streamlit_app.py
```


* ✅ Generate a **perfect `requirements.txt`** for Streamlit Cloud
* ✅ Add a **System Architecture diagram section**
* ✅ Rewrite this for **resume / internship submission / GitHub showcase**

Just tell me 😄
