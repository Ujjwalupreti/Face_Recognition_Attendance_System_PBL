import cv2
import numpy as np
import pickle
import face_recognition
from db import DatabaseService


class FaceEncoder:
    def __init__(self):
        self.db = DatabaseService()

    def retrain_model(self):
        students = self.db.get_all_students()
        known_faces, known_names, known_rolls = [], [], []

        for student in students:
            if not student["image"]:
                continue

            np_img = np.frombuffer(student["image"], np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            if img is None:
                continue

            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, boxes)

            if encodings:
                known_faces.append(encodings[0])
                known_names.append(student["names"])
                known_rolls.append(student["roll_no"])

        if not known_faces:
            print("No encodings generated, training aborted.")
            return False

        with open("ENCODE.p", "wb") as f:
            pickle.dump((known_faces, known_names, known_rolls), f)

        print(f"Model trained with {len(known_faces)} students")
        return True

    def recognize_face(frame_bytes):
        nparr = np.frombuffer(frame_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return None

        known_faces, known_names, known_rolls = [], [], []

        try:
            with open("ENCODE.p", "rb") as f:
                data = pickle.load(f)
                if isinstance(data, tuple) and len(data) == 3:
                    known_faces, known_names, known_rolls = data
        except FileNotFoundError:
            print("ENCODE.p not found. Attempting auto-train...")
            fe = FaceEncoder()
            if not fe.retrain_model():
                return None
            with open("ENCODE.p", "rb") as f:
                known_faces, known_names, known_rolls = pickle.load(f)
        except Exception as e:
            print(f"Error loading ENCODE.p: {e}")
            return None
        if not known_faces:
            print("ENCODE.p is empty or invalid.")
            return None

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        for encoding in encodings:
            matches = face_recognition.compare_faces(known_faces, encoding)
            distances = face_recognition.face_distance(known_faces, encoding)
            if len(distances) > 0:
                idx = np.argmin(distances)
                if matches[idx]:
                    return known_names[idx], known_rolls[idx]

        return None