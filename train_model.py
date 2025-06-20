#!/usr/bin/env python
"""
Independent script to train the emotion detection model.
Run this script separately when you want to train/retrain the model.

Usage: python train_model.py

Place this file in the root directory of your project (same level as manage.py)
"""

import os
import sys
import django

# Add the project directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emotion_webapp.settings')
django.setup()

# Import training functions
import tensorflow as tf
import cv2
import numpy as np
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def preprocess_image(image_path, image_size=(48, 48)):
    """Preprocess individual image for training"""
    image = cv2.imread(image_path)
    if image is None:
        return None
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray_image, image_size)
    normalized_image = resized_image.astype('float32') / 255.0
    return normalized_image

def load_images_from_directory(directory, image_size=(48, 48)):
    """Load and preprocess images from directory structure"""
    images = []
    labels = []
    class_names = []
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist!")
        return None, None, None
    
    print(f"Loading images from: {directory}")
    
    for label, class_name in enumerate(sorted(os.listdir(directory))):
        class_folder = os.path.join(directory, class_name)
        if os.path.isdir(class_folder):
            class_names.append(class_name)
            print(f"Processing class: {class_name}")
            
            image_count = 0
            for image_file in os.listdir(class_folder):
                image_path = os.path.join(class_folder, image_file)
                if image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    processed_image = preprocess_image(image_path, image_size)
                    if processed_image is not None:
                        images.append(processed_image)
                        labels.append(label)
                        image_count += 1
            
            print(f"  Loaded {image_count} images for {class_name}")
    
    print(f"Total classes found: {len(class_names)}")
    print(f"Class names: {class_names}")
    
    return np.array(images), np.array(labels), class_names

def create_and_train_model():
    """Create and train the emotion detection model"""
    
    # Dataset paths - Update these paths according to your dataset location
    train_dir = 'C:/Users/Dell/Downloads/archive/train'
    test_dir = 'C:/Users/Dell/Downloads/archive/test'
    
    print("=" * 60)
    print("EMOTION DETECTION MODEL TRAINING")
    print("=" * 60)
    
    # Check if directories exist
    if not os.path.exists(train_dir):
        print(f"Error: Training directory '{train_dir}' not found!")
        print("Please update the path in this script or ensure the dataset is in the correct location.")
        return False
    
    if not os.path.exists(test_dir):
        print(f"Warning: Test directory '{test_dir}' not found!")
        print("Will use training data for validation.")
        test_dir = None
    
    # Load training data
    print("\n1. Loading training data...")
    X_train, y_train, class_names = load_images_from_directory(train_dir)
    
    if X_train is None:
        print("Failed to load training data!")
        return False
    
    # Load test data if available
    X_test, y_test = None, None
    if test_dir:
        print("\n2. Loading test data...")
        X_test, y_test, _ = load_images_from_directory(test_dir)
        if X_test is None:
            print("Failed to load test data, will use validation split from training data.")
    
    # Reshape data
    print("\n3. Preprocessing data...")
    X_train = X_train.reshape(-1, 48, 48, 1)
    if X_test is not None:
        X_test = X_test.reshape(-1, 48, 48, 1)
    
    # Convert labels to categorical
    num_classes = len(class_names)
    y_train = to_categorical(y_train, num_classes)
    if y_test is not None:
        y_test = to_categorical(y_test, num_classes)
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Training labels shape: {y_train.shape}")
    if X_test is not None:
        print(f"Test data shape: {X_test.shape}")
        print(f"Test labels shape: {y_test.shape}")
    print(f"Number of classes: {num_classes}")
    
    # Create model
    print("\n4. Creating model architecture...")
    model = Sequential([
        Input(shape=(48, 48, 1)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("Model architecture:")
    model.summary()
    
    # Prepare validation data
    if X_test is not None and y_test is not None:
        validation_data = (X_test, y_test)
    else:
        validation_data = None
        print("Using 20% of training data for validation")
    
    # Train model
    print("\n5. Starting model training...")
    print("This may take several minutes depending on your hardware...")
    
    history = model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=32,
        validation_data=validation_data,
        validation_split=0.2 if validation_data is None else None,
        verbose=1
    )
    
    # Save model
    model_path = "emotion_detection_model.keras"
    print(f"\n6. Saving model to '{model_path}'...")
    model.save(model_path)
    
    # Save class names for later use
    class_names_path = "emotion_classes.txt"
    with open(class_names_path, 'w') as f:
        for class_name in class_names:
            f.write(f"{class_name}\n")
    
    print(f"Class names saved to '{class_names_path}'")
    
    # Display training results
    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1] if 'val_accuracy' in history.history else 0
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Final Training Accuracy: {final_train_acc:.4f}")
    print(f"Final Validation Accuracy: {final_val_acc:.4f}")
    print(f"Model saved as: {model_path}")
    print(f"Classes: {', '.join(class_names)}")
    print("\nYou can now run the Django server with:")
    print("python manage.py runserver")
    
    return True

if __name__ == "__main__":
    try:
        success = create_and_train_model()
        if success:
            print("\n✅ Training completed successfully!")
        else:
            print("\n❌ Training failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Training failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)