import cv2
import numpy as np
import face_recognition
from models.user_model import get_all_face_encodings, mark_attendance

# =============== FACE RECOGNITION UTILS ===============

def capture_face_from_webcam():
    """
    Opens webcam and captures a face image.
    Used when registering a new student.
    """
    cap = cv2.VideoCapture(0)
    print("Press 'q' to capture face...")

    face_encoding = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face locations
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            # Draw rectangle around face
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow("Capture Face - Press 'q' to Save", frame)

        # Press 'q' to capture
        if cv2.waitKey(1) & 0xFF == ord('q'):
            if face_locations:
                face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            break

    cap.release()
    cv2.destroyAllWindows()

    return face_encoding


def recognize_and_mark_attendance():
    """
    Opens webcam, recognizes faces in real-time,
    and marks attendance if student found.
    """
    known_users = get_all_face_encodings()
    known_encodings = [np.array(u["face_encoding"]) for u in known_users]
    known_ids = [u["student_id"] for u in known_users]
    known_names = [u["name"] for u in known_users]

    cap = cv2.VideoCapture(0)
    print("Press 'q' to exit attendance marking...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Resize frame for speed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    student_id = known_ids[best_match_index]
                    student_name = known_names[best_match_index]

                    # Mark attendance
                    success, msg = mark_attendance(student_id)
                    print(f"{student_name} -> {msg}")

                    # Draw rectangle with name
                    top, right, bottom, left = [v * 4 for v in face_location]  # scale back
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, student_name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (0, 255, 0), 2)

        cv2.imshow("Attendance - Press 'q' to Exit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
