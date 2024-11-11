import tensorflow as tf
import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Set root path
ROOT_PATH = r"__path__"


# Set labels
labels = {'__lable__'}

# Set parameters
BATCH_SIZE = 32
EPOCHS = 50
IMG_HEIGHT = 224
IMG_WIDTH = 224

# Load images and labels
data = []
target = []
for label in labels:
    folder_path = os.path.join(ROOT_PATH, label)
    for img_path in os.listdir(folder_path):
        img = cv2.imread(os.path.join(folder_path, img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))
        data.append(img)
        target.append(labels[label])

# Convert data to numpy array
data = np.array(data)
target = np.array(target)

# Split dataset into training and testing sets
train_data, test_data, train_target, test_target = train_test_split(
    data, target, test_size=0.2, random_state=42
)

# Preprocess data
train_data = train_data / 255.0
test_data = test_data / 255.0

# Build model for car detection
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train model
history = model.fit(
    train_data,
    train_target,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(test_data, test_target)
)


def plot(history):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.legend(loc='lower right')
    ax1.set_ylabel('Accuracy')
    ax1.set_ylim([min(min(history.history['accuracy']), min(history.history['val_accuracy'])) - 0.05, 1.05])
    ax1.set_title('Training and Validation Accuracy')
    
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Cross Entropy')
    ax2.set_ylim([0, max(max(history.history['loss']), max(history.history['val_loss'])) + 0.1])
    ax2.set_title('Training and Validation Loss')
    ax2.set_xlabel('Epoch')
    
    fig.suptitle('Model Performance', fontsize=16)
    
    plt.show()
    

# Evaluate model on test data
test_loss, test_acc = model.evaluate(test_data, test_target, verbose=2)
print('Test accuracy:', test_acc)

# Save model to file
model.save("allNewmodel.h5")
plot(history)
# Plot accuracy and loss
