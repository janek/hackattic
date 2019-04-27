import requests
import json 
from PIL import Image                                                                                
import numpy as np
from io import BytesIO
import scipy.ndimage.interpolation as interpolation
import matplotlib.pyplot as plt
import zbarlight #NOTE: might need more than pip install. see https://github.com/Polyconseil/zbarlight/

get_url = 'https://hackattic.com/challenges/reading_qr/problem?access_token=baa64683b7798b3f'
post_url = 'https://hackattic.com/challenges/reading_qr/solve?access_token=baa64683b7798b3f'

# Get the task image: 
# a QR code, placed and rotated at random on a 600x600 canvas.
response = requests.get(get_url)
img_url = response.json()['image_url']
img_data = requests.get(img_url)
img_png = Image.open(BytesIO(img_data.content))

# Read the png file, get to a single channel numpy array of 0-255 values 
img_rgba = np.array(img_png)
img = img_rgba[:,:,0]

# Trim whitespace from the canvas
def clip_whitespace(img):
    short = img[~np.all(img == 255, axis=1)]
    small = short.T[~np.all(short == 255, axis=0)].T
    return small
img = clip_whitespace(img)

# To find a reasonable position for the code:
# 1. rotate a bit, trim whitespace, check width 
# 2, minimum width is a reasonable rotation (nice_angle)

#NOTE: this is iterative search, consider binary or grqdient-like
#NOTE: this is exact to 1deg, consider making it more (or less) exact
size_sums = []
for angle in range(360):
    rotated = interpolation.rotate(img, angle, cval=255)
    clipped = clip_whitespace(rotated)
    size_sums.append(clipped.shape[0])

nice_angle = np.array(size_sums).argmin()
rotated = interpolation.rotate(img, nice_angle, cval=255)
clipped = clip_whitespace(rotated)
qr = clipped

# Convert to a format known to the qr scanner and decode
#   NOTE: the scanner is unfortunately too powerful and works for any orientation
#   (in fact, it even works for the original image).
image = Image.fromarray(qr)
codes = zbarlight.scan_codes(['qrcode'], image)
code  = str(codes[0], "utf-8")
print("Decoded: " + code)

# One of four possible 90deg rotations is the correct one
# XXX: detect the right one once qr decoder is switched to a weaker one
for angle in [90, 180, 270]:
   rotated = interpolation.rotate(qr, angle)

solution = json.dumps({"code": code})
ans = requests.post(post_url, json={"code":code})
print(ans.text)