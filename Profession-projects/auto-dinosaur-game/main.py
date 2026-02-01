from selenium import webdriver
import time
import pyautogui
from detect_dinoposition import DinosaurDetection
from detect_obstacles import ObstacleDetector
from io import BytesIO

# set up chrome
url = "https://elgoog.im/dinosaur-game/"
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option('detach', True)
chrome_option.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=chrome_option)

driver.get(url)
time.sleep(1)
pyautogui.press('space')
time.sleep(2)

while True:
    try:
        png_data = driver.get_screenshot_as_png()
        image_path = BytesIO(png_data)
        detect_manager = DinosaurDetection(image_path)
        detect_manager.detect()
        dinosaur_x = detect_manager.x_pos
        dinosaur_y = detect_manager.y_pos

        print(f"Detect dinosaur {dinosaur_x} {dinosaur_y} - {time.time()}")
        
        # Check if dinosaur was detected
        if dinosaur_x is None or dinosaur_y is None:
            driver.quit()
            exit(1)

        if dinosaur_y < 480 or dinosaur_y > 495:
            print(f"Skipping detection - dinosaur jumping (y={dinosaur_y})")
            time.sleep(0.01)
            continue

        detector = ObstacleDetector(dinosaur_x, dinosaur_y, image_path)
        detector.detect()
        jump_points = detector.jump_points
        print(f'Obstacles {detector.obstacles}, jump points {detector.jump_points}')

        for jump_point in detector.jump_points:
            distance = jump_point[0] - dinosaur_x  
            if 0 <= distance <= 250: 
                driver.switch_to.window(driver.current_window_handle)
                if jump_point[1] < dinosaur_y - 100:
                    pyautogui.press("down")
                else: 
                    pyautogui.press('space') 
                print(f"JUMPING! jump_point x={jump_point[0]}, dino x={dinosaur_x}, distance={distance}, time: {time.time()}")
                break
        time.sleep(0.01)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        break
    