import requests
import json 
from PIL import Image                                                                                
import numpy as np
import pandas as pd
import seaborn as sns
from io import BytesIO
import scipy.ndimage.interpolation as interpolation
import matplotlib.pyplot as plt

url = 'https://hackattic.com/challenges/reading_qr/problem?access_token=baa64683b7798b3f'

# Get the task image: a QR code, 
# placed and rotated at random on a 600x600 canvas.
response = requests.get(url)
img_url = response.json()['image_url']
img_data = requests.get(img_url)
img_png = Image.open(BytesIO(img_data.content))


# Read the png file, get to a single channel numpy array of zeroes and ones.
plt.imshow(img_png)
img_rgba = np.array(img_png)
img = img_rgba[:,:,0]
plt.imshow(img)

# Trim whitespace from the canvas
short = img[~np.all(img == 255, axis=1)]
small = short.T[~np.all(short == 255, axis=0)].T
img = small


# To find a reasonable position for the code:
# rotate a bit, trim whitespace, check width 
# minimum width is a reasonable rotation

#NOTE: this is iterative search, should at least be binary to be efficient
#NOTE: this is exact to 1deg, could be a bit more (esp. if binary search)
size_sums = []
for angle in range(360):
    rotated = interpolation.rotate(img, angle, cval=255)
    clipped = clip_whitespace(rotated)
    size_sums.append(clipped.shape[0])

nice_angle = np.array(size_sums).argmin()
rotated = interpolation.rotate(img, 58, cval=255)
clipped = clip_whitespace(rotated)
plt.imshow(clipped)