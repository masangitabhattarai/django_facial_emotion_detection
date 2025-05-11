import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

train_dir = 'C:/Users/Dell/Downloads/archive/train'
emotion_labels = os.listdir(train_dir)
model = tf.keras.models.load_model("emotion_detection_model.keras")

def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi_resized = cv2.resize(roi, (48, 48))
        roi_normalized = roi_resized.astype('float32') / 255.0
        roi_reshaped = roi_normalized.reshape(1, 48, 48, 1)
        prediction = model.predict(roi_reshaped)
        emotion = emotion_labels[np.argmax(prediction)]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    return frame