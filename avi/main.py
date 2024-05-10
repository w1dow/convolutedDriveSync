import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh



with mp_face_mesh.FaceMesh(
        max_num_faces=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

    cap = cv2.VideoCapture(0)

    cv2.namedWindow('Face Mesh Overlay')

    while cap.isOpened():
        success, image = cap.read()
        image = cv2.flip(image,1) 
        if not success:
            break

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            face_mesh_landmarks = results.multi_face_landmarks[0]

            annotated_image = image.copy()
            height, width, _ = annotated_image.shape 
            frame = np.zeros((height,width,3),np.uint8)
            mp_drawing.draw_landmarks(frame, face_mesh_landmarks)

            cv2.imshow('Face Mesh Overlay', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()