import logging
import os
import pathlib
import multiprocessing

import face_recognition
import numpy as np
from PIL import Image

from config import settings

logger = logging.getLogger(__name__)
FACE_DB_DIR = pathlib.Path(settings.BASE_DIR) / 'faces_db'
face_db = {}


def load_faces() -> None:
    """Load face encodings from the faces_db directory into memory."""
    global face_db
    face_db.clear()

    files = [filename for filename in os.listdir(FACE_DB_DIR) if filename.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not files:
        logger.warning("#load_faces func: No images found in faces_db directory")
        return

    num_processes = min(multiprocessing.cpu_count(), len(files))
    logger.info(f"#load_faces func: Loading faces using {num_processes} processes")

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(process_image, files)

    for name, encoding in results:
        if name and encoding is not None:
            face_db[name] = encoding

    logger.info(f"#load_faces func: Loaded {len(face_db)} faces")


def process_image(filename):
    """Processing image and return name and encoding of face"""
    try:
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = FACE_DB_DIR / filename
            name = os.path.splitext(filename)[0]
            img = Image.open(path)
            image_content_array: np.ndarray = np.array(img.convert(mode='RGB'))
            img.close()
            encodings = face_recognition.face_encodings(image_content_array)
            if encodings:
                logger.info(f"#process_image func: Loaded face: {name}")
                return name, encodings[0]
            else:
                logger.warning(f"#process_image func: No faces found in {filename}")
        return None, None
    except Exception as e:
        logger.error(f"#process_image func: Failed to process {filename}: {e}", exc_info=e)
        return None, None


def match_face(image_file) -> dict[str, bool | None]:
    """Match a face in the provided image against the face database."""
    try:
        img = face_recognition.load_image_file(image_file)
        encodings = face_recognition.face_encodings(img)
        if not encodings:
            logger.warning("#match_face func: No faces detected in uploaded image")
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
            logger.info(f"#match_face func: Face matched: {matched_id} (distance: {min_dist})")
            return {"matched": True, "person_id": matched_id}
        logger.info("#match_face func: No face match found")
        return {"matched": False, "person_id": None}
    except Exception as e:
        logger.error(f"#match_face func: Error processing image: {e}")
        return {"matched": False, "person_id": None}
