# MLP for Pima Indians Dataset Serialize to JSON and HDF5
import numpy
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

# load and evaluate a saved model
from numpy import loadtxt
from keras.models import load_model

# image params
image_size = (180, 180)
batch_size = 32
test_img_path = "testImg4.jpg"
 
# load model
model = load_model('./models/modelBackup.h5')
# summarize model.
model.summary()

# show sample
sample = mpimg.imread(test_img_path)
print(sample)
imgplot = plt.imshow(sample)
plt.show()

# process image
img = keras.preprocessing.image.load_img(
    test_img_path, target_size=image_size
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create batch axis

predictions = model.predict(img_array, verbose=1)
print(predictions)

score = predictions[0]
print(
    "This image is %.2f percent Daisy and %.2f percent Tulip."
    % (100 * (1 - score), 100 * score)
)