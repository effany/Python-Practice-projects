from PIL import Image
import numpy as np

class DinosaurDetection:
    def __init__(self, img_path):
        img = Image.open(img_path)
        self.np_array = np.array(img)
        self.x_pos = None
        self.y_pos = None
        self.half_y = self.np_array.shape[0]//2
        
    def detect(self):
        roi_y_start = self.half_y - 100
        roi = self.np_array[roi_y_start:self.half_y + 100, 30:100]
        roi_mask = (roi != [255,255,255]).any(axis=2)
        coords = np.argwhere(roi_mask)

        # Collect all dinosaur pixel coordinates
        dino_x_coords = []
        dino_y_coords = []

        for y, x in coords:
            actual_y = y + roi_y_start  # Use dynamic offset
            actual_x = x + 30   
            pixel_value = self.np_array[actual_y, actual_x]

            if np.array_equal(pixel_value, [83,83,83]): # gray scale
                dino_x_coords.append(actual_x)
                dino_y_coords.append(actual_y)
        
        # Calculate center (average of all coordinates)
        if dino_x_coords:
            self.x_pos = int(np.mean(dino_x_coords))
            self.y_pos = int(np.mean(dino_y_coords) + 5)
        else:
            print("No dinosaur detected")