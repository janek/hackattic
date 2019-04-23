import requests
import json 
from PIL import Image                                                                                
import numpy as np
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt

url = 'https://hackattic.com/challenges/reading_qr/problem?access_token=baa64683b7798b3f'

# Get the task image: a QR code, placed and rotated at random on a 600x600 canvas.
# Read the png file, get to a single channel numpy array of zeroes and ones .

response = requests.get(url)
img_url = response.json()['image_url']
img_data = requests.get(img_url)
img_png = Image.open(BytesIO(img_data.content))

img_rgba = np.array(img_png)
img_bw = img_rgba[:,:,0]
img_bw[img_bw <= 120] = 1 
img_bw[img_bw > 120] = 0

plt.imshow(img_bw)
img = img_bw


# Count length of verticals as a way of determining rotation
verticals = []
for c in range(img.shape[1]):
    first_pixel_index = 0
    last_pixel_index = 0
    for r in range(img.shape[0]):
        if img[r,c] == 1:
            if first_pixel_index == 0:
                first_pixel_index = r
            last_pixel_index = r
    vertical_length = last_pixel_index - first_pixel_index
    verticals.append(vertical_length)

print(verticals)


# Idea 1: get a vector from corner one to corner two. 
#    Use that vector to change position of every pixel?
#    Use that vector to just read things directly from QR?

# Idea 2: Rotate, check vertical lines again, rotate. 
#    Finish when vertical lines are regular (near equal) in length








