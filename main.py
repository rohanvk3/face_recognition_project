import cv2
import logging
from utils.capture import capture_frames
from utils.face_recognition_utils import detect_and_encode_faces, recognize_faces_in_frame
from utils.csv_utils import save_faces_to_csv, load_faces_from_csv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def main(source=0):
    known_encodings, _ = load_faces_from_csv()
    logging.info("Loaded known faces from CSV.")
    
    for frame in capture_frames(source):
        face_encodings = detect_and_encode_faces(frame)
        if face_encodings:
            matches = recognize_faces_in_frame(frame, known_encodings)
            for encoding, match in zip(face_encodings, matches):
                if not any(match):
                    save_faces_to_csv([encoding])
                    logging.info("Unrecognized face detected and saved to CSV.")
                    # Draw a rectangle around the detected face
                    face_locations = face_recognition.face_locations(frame)
                    for top, right, bottom, left in face_locations:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Display the frame with the rectangle
        cv2.imshow('Frame', frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
