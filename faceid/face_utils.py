import os
import face_recognition

from config import settings

FACE_DB_DIR = str(settings.BASE_DIR) + '/faces_db'
face_db = {}


def load_faces():
    global face_db
    face_db.clear()
    for filename in os.listdir(FACE_DB_DIR):
        path = os.path.join(FACE_DB_DIR, filename)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            name = os.path.splitext(filename)[0]
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                face_db[name] = encodings[0]


def match_face(image_file):
    import numpy as np
    img = face_recognition.load_image_file(image_file)
    encodings = face_recognition.face_encodings(img)
    if not encodings:
        return {"matched": False, "person_id": None}

    query = encodings[0]
    min_dist = float('inf')
    matched_id = None
    for name, known in face_db.items():
        dist = np.linalg.norm(known - query)
        if dist < min_dist:
            min_dist = dist
            matched_id = name
    if min_dist < 0.6:
        return {"matched": True, "person_id": matched_id}
    return {"matched": False, "person_id": None}
