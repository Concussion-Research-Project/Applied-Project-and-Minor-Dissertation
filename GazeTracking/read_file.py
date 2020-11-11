import numpy as np
import matplotlib as mpl
mpl.use('tkagg')    #YAAA!!  this finally makes the Damn thing work
import matplotlib.pyplot as plt

# format of the input data
x1, y1, x2, y2, xr, yr = [], [], [], [], [], []
# read from file
for line in open('eye-coordinatesFormat.txt', 'r'):
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
for line in open('eye-coordinatesBaseline.txt', 'r'):
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