import cv2
import face_recognition
import os
import csv
from datetime import datetime
import numpy as np

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
CSV_FILE = os.path.join(BASE_DIR, "attendance.csv")

print("Project Folder:", BASE_DIR)

# ---------------- LOAD KNOWN FACES ----------------
known_face_encodings = []
known_face_names = []

for file in os.listdir(IMAGE_FOLDER):
    if file.endswith(".jpg") or file.endswith(".png"):
        path = os.path.join(IMAGE_FOLDER, file)

        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(file)[0])

print("Known Faces Loaded:", known_face_names)

# ---------------- CREATE CSV FILE ----------------
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time"])

# ---------------- MARK ATTENDANCE FUNCTION ----------------
def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, date, time])

    print(f"Attendance Marked: {name} | {date} | {time}")

# ---------------- PREVENT MULTIPLE ENTRIES ----------------
already_marked = set()

# ---------------- START CAMERA ----------------
cap = cv2.VideoCapture(0)

print("\nPress 'Q' to quit\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    for (top, right, bottom, left), enc in zip(faces, encodings):

        name = "Unknown"

        if len(known_face_encodings) > 0:
            matches = face_recognition.compare_faces(known_face_encodings, enc)
            face_distances = face_recognition.face_distance(known_face_encodings, enc)

            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                if name not in already_marked:
                    mark_attendance(name)
                    already_marked.add(name)

        # Draw rectangle and name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()