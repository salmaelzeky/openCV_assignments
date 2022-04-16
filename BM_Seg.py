
def kMeansSegmentation(image, K):
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
  attempts=10
  ret,label,center=cv2.kmeans(twoDimage,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
  center = np.uint8(center)
  res = center[label.flatten()]
  kMeansSegmentation.result_image = res.reshape((image.shape))

import cv2
import numpy as np
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage


def watershedSeg(image) : 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Compute Euclidean distance from every binary pixel
    # to the nearest zero pixel then find peaks
    distance_map = ndimage.distance_transform_edt(thresh)
    local_max = peak_local_max(distance_map, indices=False, min_distance=20, labels=thresh)

    # Perform connected component analysis then apply Watershed
    markers = ndimage.label(local_max, structure=np.ones((3, 3)))[0]
    labels = watershed(-distance_map, markers, mask=thresh)

    # Iterate through unique labels
    total_area = 0
    for label in np.unique(labels):
       if label == 0:
                continue

    # Create a mask
       mask = np.zeros(gray.shape, dtype="uint8")
       mask[labels == label] = 255

    # Find contours and determine contour area
       cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
       cnts = cnts[0] if len(cnts) == 2 else cnts[1]
       c = max(cnts, key=cv2.contourArea)
       area = cv2.contourArea(c)
       total_area += area
       cv2.drawContours(image, [c], -1, (0,255,0), 3)

    print(total_area)
    a=fig.add_subplot(2,2,1)
    pl.imshow(image)

from PIL import Image # Load PIL(Python Image Library)
from google.colab.patches import cv2_imshow
import numpy as np
import cv2
from matplotlib import *
import sys
import pylab as pl
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets import make_blobs

image2 = cv2.imread('/content/fruits.jpg')
image1 = cv2.imread('/content/fruits.jpg')
image1 = cv2.cvtColor(image1,cv2.COLOR_BGR2RGB)
fig = pl.figure()
fig.set_size_inches(15,10)
watershedSeg(image2)
a=fig.add_subplot(2,2,2) # Original Color Image
kMeansSegmentation(image1, 2)
pl.imshow(kMeansSegmentation.result_image)
a=fig.add_subplot(2,2,3) # Original Color Image
kMeansSegmentation(image1, 16)
pl.imshow(kMeansSegmentation.result_image)

img = cv.imread('/content/fruits.jpg')

# filter to reduce noise
img = cv.medianBlur(img, 3)

# flatten the image
flat_image = img.reshape((-1,3))
flat_image = np.float32(flat_image)

# meanshift
bandwidth = estimate_bandwidth(flat_image, quantile=.06, n_samples=3000)
ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(flat_image)
labeled=ms.labels_


# get number of segments
segments = np.unique(labeled)
print('Number of segments: ', segments.shape[0])

# get the average color of each segment
total = np.zeros((segments.shape[0], 3), dtype=float)
count = np.zeros(total.shape, dtype=float)
for i, label in enumerate(labeled):
    total[label] = total[label] + flat_image[i]
    count[label] += 1
avg = total/count
avg = np.uint8(avg)

# cast the labeled image into the corresponding average color
res = avg[labeled]
result = res.reshape((img.shape))

# show the result
a=fig.add_subplot(2,2,4)
pl.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

def threshSeg(image):
    ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(image,127,255,cv2.THRESH_BINARY_INV)
    ret,thresh3 = cv2.threshold(image,127,255,cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(image,127,255,cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(image,127,255,cv2.THRESH_TOZERO_INV)

    titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
    images = [image, thresh1, thresh2, thresh3, thresh4, thresh5]

    xrange = range
    for i in xrange(6):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    plt.show()

import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = cv2.imread('/content/squares1.tif',0)
img2 = cv2.imread('/content/squares2.tif',0)
img3 = cv2.imread('/content/squares3.tif',0)

threshSeg(img1)
threshSeg(img2)
threshSeg(img3)
