import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("line1.jpg")
assert img is not None, "Cannot read the img"
resized_img = cv2.resize(img, (320, 240))
gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

row = gray[180].astype(np.int32)
diff = np.diff(row)
x = np.arange(len(diff))
plt.plot(x, diff)
plt.savefig("not_blurred.png")
