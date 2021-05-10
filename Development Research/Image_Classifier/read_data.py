import numpy as np
import matplotlib as mpl
from numpy.lib.function_base import append
mpl.use('tkagg')    #YAAA!!  needed to format mpl
import matplotlib.pyplot as plt
import sklearn.cluster as skcl
from pymongo import MongoClient
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # prevents keras warnings if no GPU is found on device
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model

# build a new client instance of MongoClient
mongo_client = MongoClient('mongodb+srv://research-project:cGeNVHwDOQBIjXAM@cluster0.mrfjn.mongodb.net/clients?retryWrites=true&w=majority')

# create new database and collection instance
db = mongo_client.clients
col = db.baseline
#col = db.ai_training

# test data arrays
tx1, ty1, tx2, ty2, txr, tyr = [], [], [], [], [], []

# image params
image_size = (180, 180)

"""
read_data(x1, y1, x2 , y2 , avgX , avgY)

Takes input from the user and requests the given test_id 
from the database. Upon success the dataset will be generated
into a graph and saved for classification.
"""
def read_data(v1, v2, v3 , v4 , v5 , v6):

  # enter filename to be displayed
  filename = input("Enter filename: ")

  # make an API call to the MongoDB server
  findClient = col.find_one({'client_id' : filename})

  if(findClient):
      findClient.pop("_id")
  else:
      print('\nClient with ID %s does not exists.' % (filename))

  # get contents from data result
  client_array = findClient["contents"]

  # remove new lines
  client_list_no_lines = client_array.split("\n")

  # get line from result
  for line in client_list_no_lines:
    counter = 0
    
    #remove commas
    for s in line.split(", "):
      
      # if not empty
      if(s != ""):
        value = int(s)

        # x1[] y1[] x2[] y2[]
        if(counter == 0):
          v1.append(value)
        elif(counter == 1):
          v2.append(value)
        elif(counter == 2):
          v3.append(value)
        elif(counter == 3):
          v4.append(value)
          
        counter += 1

        if(counter == 4):
          # get average (combined left and right eye)
          v5.append((v1[len(v1)-1] + v3[len(v3)-1]) / 2)
          v6.append((v2[len(v2)-1] + v4[len(v4)-1]) / 2)

  # plot average Eye Test Data
  plt.plot(v5, v6)
  # save image 
  plt.savefig('./images/plotData.jpg')
  # add title
  plt.title('Eye Test Data: ' + filename)
  # show image
  plt.show()

"""
k_means_clusters()

Converts the input data into a column stack and performs a k-means
clustering function. This groups data records into clusters of similar objects.
These clusters are then shown to the user in a series of graphs
"""
def k_means_clusters():

  # combine 4 one dimensal arrays into a 2d array
  eye_data = np.column_stack((tx1,ty1,tx2,ty2))

  # peform kmeans fitting
  kmeans = skcl.KMeans(n_clusters=5, random_state=0).fit(eye_data)

  # plot combined average data grouped by kmeans labels
  fig, axs = plt.subplots(1,2, figsize=(10,5))

  # combine 2 one dimensal arrays into a 2d array
  average_eye_data = np.column_stack((txr,tyr))

  # top left graph
  axs[0].scatter(average_eye_data[kmeans.labels_ == 0][:,0],average_eye_data[kmeans.labels_ == 0][:,1])
  axs[0].scatter(average_eye_data[kmeans.labels_ == 1][:,0],average_eye_data[kmeans.labels_ == 1][:,1])
  axs[0].scatter(average_eye_data[kmeans.labels_ == 2][:,0],average_eye_data[kmeans.labels_ == 2][:,1])
  axs[0].scatter(average_eye_data[kmeans.labels_ == 3][:,0],average_eye_data[kmeans.labels_ == 3][:,1])
  axs[0].scatter(average_eye_data[kmeans.labels_ == 4][:,0],average_eye_data[kmeans.labels_ == 4][:,1])
  axs[0].title.set_text('K-Means Cluster: Scatter')

  # top right graph
  axs[1].plot(average_eye_data[kmeans.labels_ == 0][:,0],average_eye_data[kmeans.labels_ == 0][:,1])
  axs[1].plot(average_eye_data[kmeans.labels_ == 1][:,0],average_eye_data[kmeans.labels_ == 1][:,1])
  axs[1].plot(average_eye_data[kmeans.labels_ == 2][:,0],average_eye_data[kmeans.labels_ == 2][:,1])
  axs[1].plot(average_eye_data[kmeans.labels_ == 3][:,0],average_eye_data[kmeans.labels_ == 3][:,1])
  axs[1].plot(average_eye_data[kmeans.labels_ == 4][:,0],average_eye_data[kmeans.labels_ == 4][:,1])
  axs[1].title.set_text('K-Means Cluster: Plot')
  
  # show image
  plt.show()

"""
image_classifier()

Loads the pre-trained AI model to classify the input data.
"""
def image_classifier():
  # image created from reading the input data
  test_img_path = "./images/plotData.jpg"

  # load model
  model = load_model('./ai_models/eye_data_model.h5')

  # process image
  img = keras.preprocessing.image.load_img(
      test_img_path, target_size=image_size
  )
  img_array = keras.preprocessing.image.img_to_array(img)
  img_array = tf.expand_dims(img_array, 0)  # Create batch axis

  # predict the classification
  predictions = model.predict(img_array, verbose=1)

  # show result
  score = predictions[0]
  print(
      "This image is %.2f percent Fail and %.2f percent Pass."
      % (100 * (1 - score), 100 * score)
  )

# == Run Application ==

# read test data
read_data(tx1, ty1, tx2, ty2, txr, tyr)
# peform clustering
k_means_clusters()
# classify pass/fail
image_classifier()