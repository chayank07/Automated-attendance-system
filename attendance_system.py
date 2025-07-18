import face_recognition
import cv2
import numpy as np 
import csv
from datetime import datetime
from cv2 import *

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def get_face_encodings(img_path):
    img = face_recognition.load_image_file(img_path)
    return face_recognition.face_encodings(img)[0]

def get_face_names_from_file (names):
    with open('names.txt', 'r') as f:
        names = f.read().splitlines()
    return names

face_names_file = 'names.txt'
known_face_encodings=[]
known_face_names=[]

def take_attendance_for_frame(frame, known_face_encodings, known_face_names, students, lnwriter, current_date, now):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = ""
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)
        threshold=0.45
        if matches[best_match_index]and face_distance[best_match_index]<=threshold:
            name = known_face_names[best_match_index]
            x, y, w, h = left*4, top*4, (right-left)*4, (bottom-top)*4 # Scale the coordinates back to the original frame size
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw a green rectangle around the face
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (x + 6, y - 6), font, 0.5, (255, 255, 255), 1)
            if name in known_face_names:
                if name in students:
                    students.remove(name)
                    current_time = now.strftime("%H:%M:%S")
                    lnwriter.writerow([name, current_date, current_time, "Present"])
        else:
            x, y, w, h = left*4, top*4, (right-left)*4, (bottom-top)*4 # Scale the coordinates back to the original frame size
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) # Draw a red rectangle around the face
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "Unknown", (x + 6, y - 6), font, 0.5, (255, 255, 255), 1)

    return frame, students

# Main function to continuously capture frames and take attendance
def run_attendance_system():
    known_face_encodings = []
    known_face_names = get_face_names_from_file(face_names_file)
    students = known_face_names.copy()

    for i in range(13, 20):
        img_path = f"C:\\Users\\DELL\\Desktop\\edai_project_1\\photos\\person{i}.png"
        img = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(encoding)

    current_date = datetime.now().strftime("%Y-%m-%d")
    f = open(current_date + '.csv', 'w+', newline='')
    lnwriter = csv.writer(f)
    lnwriter.writerow(["Name", "Date", "Time", "Status"])

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error reading frame")
            break
        frame, students = take_attendance_for_frame(frame, known_face_encodings, known_face_names, students, lnwriter, current_date, datetime.now())
        cv2.imshow("Attendance system", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    f.close()

run_attendance_system()