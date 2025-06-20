import tensorflow as tf
import os
import cv2
import numpy as np
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def preprocess_image(image_path, image_size=(48, 48)):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray_image, image_size)
    normalized_image = resized_image.astype('float32') / 255.0
    return normalized_image

def load_images_from_directory(directory, image_size=(48, 48)):
    images = []
    labels = []
    for label, class_name in enumerate(os.listdir(directory)):
        class_folder = os.path.join(directory, class_name)
        if os.path.isdir(class_folder):
            for image_file in os.listdir(class_folder):
                image_path = os.path.join(class_folder, image_file)
                if image_path.endswith(('.jpg', '.jpeg', '.png')):
                    processed_image = preprocess_image(image_path, image_size)
                    images.append(processed_image)
                    labels.append(label)
    return np.array(images), np.array(labels)

def create_and_train_model():
    """Function to create and train the emotion detection model"""
    train_dir = 'C:/Users/Dell/Downloads/archive/train'
    test_dir = 'C:/Users/Dell/Downloads/archive/test'
    
    X_train, y_train = load_images_from_directory(train_dir)
    X_test, y_test = load_images_from_directory(test_dir)

    X_train = X_train.reshape(-1, 48, 48, 1)
    X_test = X_test.reshape(-1, 48, 48, 1)

    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")

    model = Sequential([
        Input(shape=(48, 48, 1)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(y_train.shape[1], activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test))

    model.save("emotion_detection_model.keras")
    print("Model training completed and saved!")

# Only run training if this script is executed directly
if __name__ == "__main__":
    create_and_train_model()