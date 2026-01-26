import numpy as np
from PIL import Image

class ObstacleDetector:
    def __init__(self, dino_x, dino_y, img_path):
        img = Image.open(img_path)
        self.np_array = np.array(img)
        self.dino_x = dino_x
        self.dino_y = dino_y
        self.roi = self.np_array[self.dino_y - 100: self.dino_y + 5, self.dino_x + 100:self.np_array.shape[1]]
        self.max_obstacle_x = None
        self.min_obstacle_x = None
        self.obstacles = []
        self.jump_points = []

    def detect(self):
        roi_mask = (self.roi != [255, 255, 255]).all(axis=2)
        coords = np.argwhere(roi_mask)
        np.set_printoptions(threshold=np.inf)

        # Collect all data first - filter by pixel color (only dark obstacles)
        data = []
        for y, x in coords:
            actual_y = (self.dino_y - 100) + y
            actual_x = (self.dino_x + 100) + x
            pixel_value = self.np_array[actual_y, actual_x]
            # Only include dark pixels (obstacles) - exclude light gray ground lines
            # Obstacles are typically dark (close to [83,83,83] or darker)
            if np.mean(pixel_value) < 150:  # Dark pixels only
                data.append((actual_y, actual_x, pixel_value))

        if data:
            self.min_obstacle_x = min(data, key=lambda item: item[1])[1]
            self.max_obstacle_x = max(data, key=lambda item: item[1])[1]

        x_start_checkpoint = self.min_obstacle_x
        obstacles = []

        while x_start_checkpoint <= self.max_obstacle_x:
            items_in_range = [item for item in data if x_start_checkpoint <= item[1] < x_start_checkpoint + 150]
            if items_in_range:
                smallest_x_item = min(items_in_range, key=lambda item: item[1])
                smallest_x_in_group = smallest_x_item[1]  # x value
                correspond_y = smallest_x_item[0]  # y value of that same point
                obstacles.append([int(smallest_x_in_group), int(correspond_y)])
            x_start_checkpoint += 100

        self.obstacles = obstacles
        self.jump_points = [[item[0] - 100, item[1]] for item in self.obstacles]