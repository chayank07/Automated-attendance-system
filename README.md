# 🕵️ Automated Attendance System using Face Recognition

A Python-based attendance system using OpenCV and face recognition. It captures faces via webcam, recognizes them, and logs attendance to a CSV file.

## 🛠 Technologies Used
- Python
- OpenCV
- face_recognition library
- CSV for logging

## 📁 How It Works
1. Load known faces from `photos/`
2. Start webcam
3. Detect and recognize face
4. Log attendance to `attendance.csv`

Note: Real person data/images used during testing have been removed for privacy compliance.

## ▶️ Run It

```bash
pip install -r requirements.txt
python attendance_system.py
