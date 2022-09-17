#!/usr/bin/python3
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("line1.jpg")
assert img is not None, "Cannot read the img"
resized_img = cv2.resize(img, (320, 240))

gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
blurred = cv2.blur(gray, (3,3))

row = gray[180].astype(np.int32)
diff = np.diff(row)
x = np.arange(len(diff))
plt.plot(x, diff)
plt.savefig("not_blurred.png")

# row = blurred[180].astype(np.int32)
# diff = np.diff(row)
# x = np.arange(len(diff))
# plt.plot(x, diff)
# plt.savefig("blurred.png")

max_diff = np.amax(diff, 0)
min_diff = np.amin(diff, 0)
max_diff_index = np.where(diff == max_diff)[0][0]
min_diff_index = np.where(diff == min_diff)[0][0]
print(max_diff, max_diff_index, min_diff, min_diff_index)
middle = (min_diff_index + max_diff_index) // 2
print(middle)
plt.plot([middle, middle], [min_diff, max_diff], 'r-')
plt.plot([min_diff_index, min_diff_index], [min_diff, max_diff], 'g--')
plt.plot([max_diff_index, max_diff_index], [min_diff, max_diff], 'g--')
plt.savefig("located_lines.png")