import numpy as np
import matplotlib as mpl
mpl.use('tkagg')    #YAAA!!  this finally makes the Damn thing work
import matplotlib.pyplot as plt
import math
import sklearn.cluster as skcl
from mpl_toolkits.mplot3d import axes3d


# =========== test code ===============



# ==== plot data in a graph for visualiation ====
# format of the input data
x1, y1, x2, y2, xr, yr = [], [], [], [], [], []
# read from file
# for line in open('eye-coordinatesFormat.txt', 'r'):
# for line in open('object_rocket.csv', 'r'):
for line in open('eye-coordinates.txt', 'r'):
  values = [float(s) for s in line.split()]
  x1.append(values[0])
  y1.append(values[1])
  x2.append(values[2])
  y2.append(values[3])
  xr.append((values[0] + values[2]) / 2)
  yr.append((values[1] + values[3]) / 2)


# Test Data: Both Eyes
plt.plot(x1, y1)
plt.plot(x2, y2)
plt.show()

# Test Data: Average
plt.plot(xr, yr)
plt.show()


# baseline data
bx1, by1, bx2, by2, bxr, byr = [], [], [], [], [], []
for line in open('eye-coordinatesBaseLine.txt', 'r'):
  values = [float(s) for s in line.split()]
  bx1.append(values[0])
  by1.append(values[1])
  bx2.append(values[2])
  by2.append(values[3])
  bxr.append((values[0] + values[2]) / 2)
  byr.append((values[1] + values[3]) / 2)


# Baseline Data: Both Eyes
plt.plot(bx1, by1)
plt.plot(bx2, by2)
plt.show()

# Baseline Data: Average
plt.plot(bxr, byr)
plt.show()

# Test Average vs Baseline Average
plt.plot(bxr, byr)
plt.plot(xr, yr)
plt.show()


# ==== work out standard deviation for tests and baseline====

# tests
# std xr
stdXr = np.std(xr)
print("stdXr : ", stdXr)

# std yr
stdYr = np.std(yr)
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

# ==== scikit-learn ======
# k-means clustering

# load in dataset
eye_data = np.genfromtxt('eye-coordinatesBaseLine.txt', delimiter=' ', usecols=(0,1,2,3), skip_header=0)

# create 4d graph
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# plot eye data
img = ax.scatter(eye_data[:,0], eye_data[:,1], eye_data[:,2], c=eye_data[:,3], cmap=plt.hot())
fig.colorbar(img)
plt.show()

# create a 3d graph
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# plot eye data
img = ax.scatter(eye_data[:,0], eye_data[:,1], eye_data[:,2])
plt.show()

# peform kmeans fitting
kmeans = skcl.KMeans(n_clusters=5, random_state=0).fit(eye_data)

# display cluster labels
print(kmeans.labels_)

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
average_eye_data = np.column_stack((xr,yr))

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













