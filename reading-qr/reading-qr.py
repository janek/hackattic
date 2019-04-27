import requests
import json 
from PIL import Image                                                                                
import numpy as np
from io import BytesIO
import scipy.ndimage.interpolation as interpolation
import matplotlib.pyplot as plt
import zbarlight #NOTE: might need more than pip install. see https://github.com/Polyconseil/zbarlight/

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
def clip_whitespace(img):
    short = img[~np.all(img == 255, axis=1)]
    small = short.T[~np.all(short == 255, axis=0)].T
    return small
img = clip_whitespace(img)

# To find a reasonable position for the code:
# 1. rotate a bit, trim whitespace, check width 
# 2, minimum width is a reasonable rotation (nice_angle)

#NOTE: this is iterative search, should at least be binary to be efficient
#NOTE: this is exact to 1deg, we could consider making it more (or less) exact
size_sums = []
for angle in range(360):
    rotated = interpolation.rotate(img, angle, cval=255)
    clipped = clip_whitespace(rotated)
    size_sums.append(clipped.shape[0])

nice_angle = np.array(size_sums).argmin()
rotated = interpolation.rotate(img, nice_angle, cval=255)
clipped = clip_whitespace(rotated)
plt.imshow(clipped)
qr = clipped


# Convert to a format known to the qr scanner and decode
#   NOTE: the scanner is unfortunately too powerful and works for any orientation
#   (in fact, it even works for the original image).
image = Image.fromarray(qr)
codes = zbarlight.scan_codes(['qrcode'], image)


print(codes)

# One of four possible 90deg rotations is the correct one
# XXX: detect the right one once qr decoder is switched to a weaker one
for angle in [90, 180, 270]:
   rotated = interpolation.rotate(qr, angle)
