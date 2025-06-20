import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

# Load trained model
model_path = "C:/Users/Dell/emotion_detection_model.h5"
if os.path.exists(model_path):
    model = load_model(model_path)
else:
    print(f"Model file '{model_path}' not found. Exiting.")
    exit(1)

# Load emotion labels from file
emotion_labels = []
class_file = "emotion_classes.txt"
if os.path.exists(class_file):
    with open(class_file, 'r') as f:
        emotion_labels = [line.strip() for line in f.readlines()]
else:
    # fallback labels if file missing
    emotion_labels = ['angry', 'happy', 'neutral', 'sad']
    print(f"Warning: '{class_file}' not found. Using default labels.")

# Initialize face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi_resized = cv2.resize(roi, (48, 48))
        roi_normalized = roi_resized.astype('float32') / 255.0
        roi_reshaped = roi_normalized.reshape(1, 48, 48, 1)

        try:
            prediction = model.predict(roi_reshaped, verbose=0)
            emotion_index = np.argmax(prediction)
            emotion = emotion_labels[emotion_index]
        except Exception as e:
            emotion = "Error"
            print(f"Prediction error: {e}")

        # Draw rectangle around face and put emotion label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (36, 255, 12), 2)

    return frame

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame_with_emotion = detect_emotion(frame)
        cv2.imshow('Emotion Detector', frame_with_emotion)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
