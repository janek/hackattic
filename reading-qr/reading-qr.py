import requests
import json 
from PIL import Image                                                                                
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import cv2

# https://matplotlib.org/users/image_tutorial.html


url = 'https://hackattic.com/challenges/reading_qr/problem?access_token=baa64683b7798b3f'

response = requests.get(url)
img_url = response.json()['image_url']
img_data = requests.get(img_url)
img_png = Image.open(BytesIO(img_data.content))
img_rgba = np.array(img_png)

r = img_rgba[:,:,0]
(r == 255).sum()
(r == 0).sum()
(r == 255).sum() + (r == 0).sum() - len(r.ravel())




