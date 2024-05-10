import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh



# Initialize MediaPipe face mesh model
with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=100,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

    # OpenCV video capture
    cap = cv2.VideoCapture(0)

    # Create OpenCV windows
    cv2.namedWindow('Face Mesh Overlay')

    while cap.isOpened():
        success, image = cap.read()
        # cv2.flip(image)
        if not success:
            break

        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and get face mesh data
        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            # Extract mesh data
            face_mesh_landmarks = results.multi_face_landmarks[0]

            # Draw face mesh
            annotated_image = image.copy()
            height, width, _ = annotated_image.shape 
            frame = np.zeros((height,width,3),np.uint8)
            mp_drawing.draw_landmarks(frame, face_mesh_landmarks)

            # Show annotated image with face mesh overlay
            cv2.imshow('Face Mesh Overlay', frame)

        # Show original video feed
        # cv2.imshow('Video Feed', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()