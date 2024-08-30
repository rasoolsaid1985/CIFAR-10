# -*- coding: utf-8 -*-
"""CIFAR-10 DenseNet121.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yCYvfZjWJb8i3AOICEBZEq4jx0pLZQa0
"""

!kaggle competitions download -c titanic
!kaggle datasets download -d catmanjr/cifar-10-train-valid-test

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import cv2
import keras
import tensorflow as tf
import tensorflow.keras.layers as layers
import tensorflow.keras.models as models
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.applications as applications
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, BatchNormalization
from keras.models import Sequential, load_model
from tensorflow.keras.models import Model
import tensorflow.keras.callbacks as callbacks
import tensorflow.keras.utils as utils
from tensorflow.keras.applications import DenseNet121, ResNet152V2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input

zip_path = 'cifar-10-train-valid-test.zip'
!unzip -q {zip_path}
zip_path = '/content'

train_dir = '/content/train_valid_test/train_valid_test/train'
valid_dir = '/content/train_valid_test/train_valid_test/valid'

image_size = [64,64]
batch_size = 32

base_model = applications.DenseNet121(input_shape=(64,64,3), weights='imagenet', include_top=False)

# base_model.trainable = False

for layers in base_model.layers:
  layers.trainable = False

datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize pixel values
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
train_ds = keras.utils.image_dataset_from_directory(
    directory=train_dir,
    labels='inferred',
    label_mode='categorical',
    batch_size=batch_size,
    image_size=image_size,

)
valid_ds = keras.utils.image_dataset_from_directory(
    directory=valid_dir,
    labels='inferred',
    label_mode='categorical',
    batch_size=batch_size,
    image_size=image_size,
)

def process(image, label):
  image = tf.cast(image/255.0, tf.float32)
  return image, label

train_ds = train_ds.map(process)
valid_ds = valid_ds.map(process)

inputs = Input(shape=(64, 64, 3))

# Pass the inputs through the base model
x = base_model(inputs, training=False)

# Add global average pooling
x = GlobalAveragePooling2D()(x)

# Add a dense layer
x = Dense(1024, activation='relu')(x)

# Add the output layer
outputs = Dense(10, activation='softmax')(x)

# Create the model
model = Model(inputs, outputs)

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Display the model summary
model.summary()

history = model.fit(train_ds, validation_data=valid_ds, epochs=10)

model.save('model.h5')

loss, accuracy = model.evaluate(valid_ds)
print(f'Validation Loss: {loss:.4f}')
print(f'Validation Accuracy: {accuracy:.4f}')

from tensorflow.keras.preprocessing import image
import numpy as np

def load_and_preprocess_image(img_path, target_size):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize
    return img_array

img_path = '/content/train_valid_test/train_valid_test/train/ship/14582.png'
img_array = load_and_preprocess_image(img_path, target_size=(64, 64))

predictions = model.predict(img_array)
predicted_class = np.argmax(predictions[0])
print(f'Predicted class index: {predicted_class}')

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
predicted_class_label = class_names[predicted_class]
print(f'Predicted class label: {predicted_class_label}')

import matplotlib.pyplot as plt

# Load and display the image
img = image.load_img(img_path, target_size=(64, 64))
plt.imshow(img)
plt.title(f'Predicted: {predicted_class_label}')
plt.axis('off')
plt.show()
