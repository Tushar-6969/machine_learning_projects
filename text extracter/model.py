import os
import sys
import json
import traceback
import cv2
import numpy as np
import tensorflow as tf

# Constants
MODEL_PATH = 'ocr_model.h5'
UPLOAD_FOLDER = 'uploads'
MAX_LABEL_LENGTH = 16
CHARS = "abcdefghijklmnopqrstuvwxyz0123456789 "  # Modify based on your charset

CHAR_TO_INDEX = {c: i for i, c in enumerate(CHARS)}
INDEX_TO_CHAR = {i: c for c, i in CHAR_TO_INDEX.items()}

# Create upload folder if needed
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Image preprocessing
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (128, 32))  # Resize to fit model input size
    image = image.astype(np.float32) / 255.0  # Normalize
    image = np.expand_dims(image, axis=-1)  # HWC
    return np.expand_dims(image, axis=0)    # B, H, W, C

# Model architecture (simplified for illustration)
def create_model(input_shape=(32, 128, 1), num_classes=len(CHARS)):
    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same')(inputs)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Reshape((-1, x.shape[-1] * x.shape[-2]))(x)  # Time x Features
    x = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True))(x)
    x = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
    model = tf.keras.Model(inputs, x)
    return model

# Dummy label generation
def dummy_label(text, max_length=MAX_LABEL_LENGTH):
    label = [CHAR_TO_INDEX.get(c, 0) for c in text.lower() if c in CHAR_TO_INDEX]
    label += [0] * (max_length - len(label))  # pad
    return np.array(label[:max_length])

# Load the model if it exists, or train it if not
def load_or_train_model():
    if os.path.exists(MODEL_PATH):
        print("Loading model...")
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    else:
        print("Training model...")
        model = create_model()
        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        # Assume you have a dataset for training here (modify accordingly)
        X, Y = load_training_data(UPLOAD_FOLDER)
        model.fit(X, Y, epochs=10, batch_size=8, verbose=1)
        model.save(MODEL_PATH)
    return model

# Predict text from an image
def predict_text(image_path):
    image = preprocess_image(image_path)
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    preds = model.predict(image)[0]
    indices = np.argmax(preds, axis=1)
    return "".join([INDEX_TO_CHAR.get(i, "") for i in indices]).strip()

# Handle the training data (load the images, this should be tailored to your dataset)
def load_training_data(dataset_path, max_samples=200):
    # You need to adapt this part to your dataset (reading image files and labels)
    pass

# Entry point
if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise ValueError("Usage: python model.py <image_path>")

        image_path = sys.argv[1]

        model = load_or_train_model()

        # Predict text
        predicted_text = predict_text(image_path)

        # Return the output in JSON format
        result = {
            "custom_model": predicted_text
        }
        print(json.dumps(result))  # This will be captured by the Node.js server

    except Exception as e:
        # In case of error, provide the error message in JSON
        result = {
            "error": str(e),
            "trace": traceback.format_exc()
        }
        print(json.dumps(result))
