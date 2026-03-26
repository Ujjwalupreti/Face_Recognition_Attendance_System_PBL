# 📸 Face Recognition Attendance System

![Face Attendance Banner](https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=300&section=header&text=Face%20Attendance%20System&fontSize=60&animation=fadeIn&fontAlignY=35&desc=Contactless%20Biometrics%20%7C%20Real-Time%20Tracking%20%E2%80%A2%20Automated%20Pipelines&descAlignY=60&descSize=20)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![JavaScript](https://img.shields.io/badge/Frontend-Vanilla_JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![OpenCV](https://img.shields.io/badge/Computer_Vision-OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)

> **A Seamless, AI-Powered Attendance Management Platform utilizing facial biometrics for contactless, real-time student tracking and analytics.**

## 📌 Project Overview
The **Face Recognition Attendance System** is a modern web application designed to eliminate manual roll calls and proxy attendance. By leveraging Computer Vision (`face_recognition` & `OpenCV`), it processes live webcam feeds directly from the browser to identify students and securely log their presence into a relational database.

The platform centralizes the onboarding, recognition, and reporting processes, offering a frictionless experience for both administrators and students.

### 🎯 Key Features
* **🤖 Dynamic Model Orchestration:** Automatically extracts 128-dimensional facial encodings upon new student registration and updates the serialized AI model in real-time.
* **📸 Contactless Real-Time Capture:** Integrates HTML5 WebRTC for live, browser-based face capture with automated frame extraction.
* **🛡️ Smart Attendance Logic:** Implements time-aware database constraints to prevent duplicate daily attendance entries.
* **📊 Analytics & Export Dashboard:** Visualizes 45-day attendance ratios using `Chart.js` and allows one-click CSV report generation.

---

## ⚙️ Technology Stack

| Component | Tech Stack | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, ES6 Modules | Glassmorphism UI, MediaDevices API for WebRTC, Chart.js |
| **Backend** | Flask (Python) | Lightweight WSGI web application framework with CORS |
| **Database** | MySQL | Relational storage for Student BLOBs, Profiles, and Timestamps |
| **AI / ML** | OpenCV, `face_recognition` | Dlib-based facial detection and metric learning (ResNet) |

---

## 🔄 System Architecture & Workflow

The application follows a modular architecture, securely separating the browser's media hardware from the heavy biometric processing on the backend server.

1. **Student Onboarding:** User submits details and a reference image. Flask converts the image to binary (`LONGBLOB`) and stores it in MySQL.
2. **Biometric Bootstrapping:** Backend reads the new BLOB, decodes it via OpenCV, extracts facial vectors, and serializes the state to an `ENCODE.p` file.
3. **Live Recognition:** React/Vanilla JS accesses the webcam, captures a snapshot via `<canvas>`, and POSTs the payload to the server.
4. **Validation & Logging:** The server compares the live frame against the `.p` file. If a match is found and no prior attendance exists for today, the SQL log is updated.

---

## 🧠 Biometric Processing & Data Pipeline
> **Theme:** Automated Facial Encoding Pipeline with Fault Tolerance

Handling live image data and maintaining a continuously updating ML model requires careful state management. This project implements resilient **Data Engineering & Computer Vision** principles to ensure the system doesn't crash during edge cases (e.g., missing faces, corrupted files).

### 🛡️ Implemented ML Controls

#### 1️⃣ Deep Metric Learning (Facial Encodings)
* **Mechanism:** Converts human faces into a 128-dimensional vector space using a pre-trained ResNet network.
* **Matching Logic:** Uses Euclidean distance to compare the live frame's vector against all known vectors. The lowest distance (below a strict threshold) triggers an identity match.

#### 2️⃣ Automated Fault-Tolerant Training
* **Auto-Recovery:** If the server restarts and `ENCODE.p` is missing, the `FaceEncoder` automatically triggers a `retrain_model()` sequence, querying the MySQL database to rebuild the model from scratch on the fly.
* **Atomic Rollbacks:** If a new student registers but the AI fails to find a face in their uploaded image, the database immediately deletes the corrupted user record to maintain systemic integrity.

#### 3️⃣ Efficient Memory Handling
* **In-Memory Decoding:** Web uploads and SQL BLOBs are decoded directly into OpenCV arrays using `np.frombuffer` and `cv2.imdecode`, eliminating the need to read/write temporary physical image files to the server disk.

### 📊 System Resilience Analysis
| System Challenge | Mitigation Strategy | Result |
| :--- | :--- | :--- |
| **Duplicate Attendance Marking** | SQL Date-level validation (`DATE(date_time) = DATE(now)`) | Proxies and double-clicks blocked |
| **Missing/Corrupted ML Model** | Fallback auto-training block in `recognize_face` | Zero-downtime model recovery |
| **Hardware Latency / Memory Leaks** | Frontend `setTimeout` & stream track stopping | Webcam auto-releases after 15 seconds |
| **No Face in Uploaded Image** | Encoding length validation | Aborts training; prevents false positives |

---

## 🚀 Future Roadmap

### 🧠 Computer Vision Enhancements
- [ ] **Liveness Detection:** Implement blink/smile detection or depth analysis to prevent spoofing via printed photos or phone screens.
- [ ] **Multi-Face Tracking:** Upgrade the `/capture` endpoint to process and mark attendance for multiple students in a single classroom frame.

### 💻 Application Features
- [ ] **Dockerization:** Containerize the Flask API and MySQL instance using `docker-compose` for 1-click deployments.
- [ ] **Admin Dashboard:** Add a secure login portal for teachers to manually edit attendance or delete graduates.

---

## 👥 Contributors
* **Ujjwal Upreti**
* **Vaibhav Joshi** 
* **Lokesh Joshi**
