import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter

class ColourExtractMaganer:
    def __init__(self, img_path):
        img = Image.open(img_path)
        np_array = np.array(img)
        all_colors = []
        pixels = np_array.reshape(-1, 4)
        
        for pixel in pixels:
            rgba = (int(pixel[0]), int(pixel[1]), int(pixel[2]), int(pixel[3]))
            all_colors.append(rgba)
        
        color_counts = Counter(all_colors)
        self.all_colors = [color for color, count in color_counts.most_common(25)]






