import os
import random
import matplotlib.pyplot as plt
from PIL import Image

img_dir = r'C:\Users\sofis\Downloads\Untitled-1 (1)\Data\Bs4_Images_resized'

img_files = [f for f in os.listdir(img_dir) if f.endswith('.jpg') or f.endswith('.png')]

sample_imgs = random.sample(img_files, 15)
plt.subplots_adjust(wspace=0.1, hspace=0.2)
fig, axes = plt.subplots(nrows=5, ncols=3, figsize=(10,15))

for i, ax in enumerate(axes.flat):
    img = Image.open(os.path.join(img_dir, sample_imgs[i]))
    ax.imshow(img)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(sample_imgs[i])
    
# display the plot
plt.show()
