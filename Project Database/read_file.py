import numpy as np
import matplotlib as mpl
from numpy.lib.function_base import append
mpl.use('tkagg')    #YAAA!!  this finally makes the Damn thing work
import matplotlib.pyplot as plt
import math
import sklearn.cluster as skcl
from mpl_toolkits.mplot3d import axes3d
from pymongo import MongoClient

# build a new client instance of MongoClient
mongo_client = MongoClient('mongodb+srv://research-project:cGeNVHwDOQBIjXAM@cluster0.mrfjn.mongodb.net/clients?retryWrites=true&w=majority')

# create new database and collection instance
db = mongo_client.clients
col = db.baseline

# test data arrays
tx1, ty1, tx2, ty2, txr, tyr = [], [], [], [], [], []

# baseline data arrays
bx1, by1, bx2, by2, bxr, byr = [], [], [], [], [], []


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

  # Test Data: Both Eyes
  plt.plot(v1, v2)
  plt.plot(v3, v4)
  plt.show()

  # Test Data: Average
  plt.plot(v5, v6)
  plt.show()

# read test data
read_data(tx1, ty1, tx2, ty2, txr, tyr)

# read baseline data
read_data(bx1, by1, bx2, by2, bxr, byr)

# Test Average vs Baseline Average
plt.plot(bxr, byr)
plt.plot(txr, tyr)
plt.show()

# tests
stdXr = np.std(txr)
print("stdXr : ", stdXr)

# std yr
stdYr = np.std(tyr)
print("stdYr : ", stdYr)

# combine std of 2 dimensions
stdXrYr = math.sqrt(math.pow(stdXr, 2) + math.pow(stdYr, 2))
print("stdXrYr : ", stdXrYr)

#baseline
# std xr
stdbXr = np.std(bxr)
print("stdbXr : ", stdbXr)

# std yr
stdbYr = np.std(byr)
print("stdbYr : ", stdbYr)

# combine std of 2 dimensions
stdbXrYr = math.sqrt(math.pow(stdbXr, 2) + math.pow(stdbYr, 2))
print("stdXrYr : ", stdbXrYr)

# calculate percentage difference
# dif = (v1 - v2)/((v1 + v2) / 2) * 100
dif = abs(((stdXrYr - stdbXrYr)/((stdXrYr + stdbXrYr)/2)) * 100)
print("Percent Difference : ", dif)

# decide pass/fail (allow 5% margin of error)
if(dif < 5):
  print("Pass...")
else:
  print("Fail...")

# combine 4 one dimensal arrays into a 2d array
eye_data = np.column_stack((tx1,ty1,tx2,ty2))

# create 4d graph
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# plot eye data
img = ax.scatter(eye_data[:,0], eye_data[:,1], eye_data[:,2], c=eye_data[:,3], cmap=plt.hot())
fig.colorbar(img)
plt.show()

# peform kmeans fitting
kmeans = skcl.KMeans(n_clusters=5, random_state=0).fit(eye_data)

# display cluster labels
print("Cluster Labels: ", kmeans.labels_)

# make a 3d plot using cluster labels
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# plot eye data grouped by kmeans labels
img = ax.scatter(eye_data[kmeans.labels_ == 0][:,0], eye_data[kmeans.labels_ == 0][:,1], eye_data[kmeans.labels_ == 0][:,2])
img = ax.scatter(eye_data[kmeans.labels_ == 1][:,0], eye_data[kmeans.labels_ == 1][:,1], eye_data[kmeans.labels_ == 1][:,2])
img = ax.scatter(eye_data[kmeans.labels_ == 2][:,0], eye_data[kmeans.labels_ == 2][:,1], eye_data[kmeans.labels_ == 2][:,2])
img = ax.scatter(eye_data[kmeans.labels_ == 3][:,0], eye_data[kmeans.labels_ == 3][:,1], eye_data[kmeans.labels_ == 3][:,2])
img = ax.scatter(eye_data[kmeans.labels_ == 4][:,0], eye_data[kmeans.labels_ == 4][:,1], eye_data[kmeans.labels_ == 4][:,2])
plt.show()

# make 2d plots
fig, axs = plt.subplots(2,2, figsize=(10,10))

# top left fig
axs[0,0].scatter(eye_data[kmeans.labels_ == 0][:,0],eye_data[kmeans.labels_ == 0][:,1])
axs[0,0].scatter(eye_data[kmeans.labels_ == 1][:,0],eye_data[kmeans.labels_ == 1][:,1])
axs[0,0].scatter(eye_data[kmeans.labels_ == 2][:,0],eye_data[kmeans.labels_ == 2][:,1])
axs[0,0].scatter(eye_data[kmeans.labels_ == 3][:,0],eye_data[kmeans.labels_ == 3][:,1])
axs[0,0].scatter(eye_data[kmeans.labels_ == 4][:,0],eye_data[kmeans.labels_ == 4][:,1])

# top right fig
axs[0,1].scatter(eye_data[kmeans.labels_ == 0][:,2],eye_data[kmeans.labels_ == 0][:,3])
axs[0,1].scatter(eye_data[kmeans.labels_ == 1][:,2],eye_data[kmeans.labels_ == 1][:,3])
axs[0,1].scatter(eye_data[kmeans.labels_ == 2][:,2],eye_data[kmeans.labels_ == 2][:,3])
axs[0,1].scatter(eye_data[kmeans.labels_ == 3][:,2],eye_data[kmeans.labels_ == 3][:,3])
axs[0,1].scatter(eye_data[kmeans.labels_ == 4][:,2],eye_data[kmeans.labels_ == 4][:,3])

# bottom left fig
axs[1,0].plot(eye_data[kmeans.labels_ == 0][:,0],eye_data[kmeans.labels_ == 0][:,1])
axs[1,0].plot(eye_data[kmeans.labels_ == 1][:,0],eye_data[kmeans.labels_ == 1][:,1])
axs[1,0].plot(eye_data[kmeans.labels_ == 2][:,0],eye_data[kmeans.labels_ == 2][:,1])
axs[1,0].plot(eye_data[kmeans.labels_ == 3][:,0],eye_data[kmeans.labels_ == 3][:,1])
axs[1,0].plot(eye_data[kmeans.labels_ == 4][:,0],eye_data[kmeans.labels_ == 4][:,1])

# bottom right fig
axs[1,1].plot(eye_data[kmeans.labels_ == 0][:,2],eye_data[kmeans.labels_ == 0][:,3])
axs[1,1].plot(eye_data[kmeans.labels_ == 1][:,2],eye_data[kmeans.labels_ == 1][:,3])
axs[1,1].plot(eye_data[kmeans.labels_ == 2][:,2],eye_data[kmeans.labels_ == 2][:,3])
axs[1,1].plot(eye_data[kmeans.labels_ == 3][:,2],eye_data[kmeans.labels_ == 3][:,3])
axs[1,1].plot(eye_data[kmeans.labels_ == 4][:,2],eye_data[kmeans.labels_ == 4][:,3])
plt.show()

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

# top right graph
axs[1].plot(average_eye_data[kmeans.labels_ == 0][:,0],average_eye_data[kmeans.labels_ == 0][:,1])
axs[1].plot(average_eye_data[kmeans.labels_ == 1][:,0],average_eye_data[kmeans.labels_ == 1][:,1])
axs[1].plot(average_eye_data[kmeans.labels_ == 2][:,0],average_eye_data[kmeans.labels_ == 2][:,1])
axs[1].plot(average_eye_data[kmeans.labels_ == 3][:,0],average_eye_data[kmeans.labels_ == 3][:,1])
axs[1].plot(average_eye_data[kmeans.labels_ == 4][:,0],average_eye_data[kmeans.labels_ == 4][:,1])

plt.show()

