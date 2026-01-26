# Auto Dinosaur Game Bot

## Overview
This project implements an automated bot that plays the Chrome Dinosaur Game using computer vision and Selenium WebDriver. The bot detects the dinosaur's position, identifies obstacles, and automatically makes the dinosaur jump or duck to avoid them.

## Project Architecture

### File Structure
```
auto-dinosaur-game/
├── main.py                    # Main game loop and automation logic
├── detect_dinoposition.py     # Dinosaur position detection
├── detect_obstacles.py        # Obstacle detection and jump point calculation
└── README.md                  # Project documentation
```

## Core Components

### 1. Main Controller (`main.py`)

**Purpose**: Orchestrates the entire automation process by capturing screenshots, detecting objects, and controlling the dinosaur.

**Key Technologies**:
- **Selenium WebDriver**: Browser automation and screenshot capture
- **PyAutoGUI**: Simulates keyboard inputs (space/down arrows)
- **PIL (Pillow)**: Image processing
- **NumPy**: Array operations for image analysis

**Main Loop Logic**:
1. Initialize Chrome browser with the dinosaur game
2. Continuously capture screenshots as PNG data
3. Detect dinosaur position in each frame
4. Detect obstacles and calculate jump points
5. Execute jump or duck actions based on distance thresholds
6. Handle errors and exit gracefully

**Key Variables**:
- `dinosaur_x`, `dinosaur_y`: Current position of the dinosaur
- `jump_points`: List of X,Y coordinates where jumps should be triggered
- `distance`: Gap between dinosaur and obstacle (0-250 pixels = action zone)

**Action Logic**:
- If obstacle Y-position is 50+ pixels above dinosaur: Press **DOWN** (duck)
- Otherwise: Press **SPACE** (jump)
- Action triggered when obstacle is within 0-250 pixels distance

---

### 2. DinosaurDetection Class (`detect_dinoposition.py`)

**Purpose**: Locates the dinosaur's center position in the game screenshot.

#### Class Structure

```python
class DinosaurDetection:
    def __init__(self, img_path)
    def detect(self)
```

#### Attributes
- `np_array`: NumPy array representation of the screenshot
- `x_pos`: Horizontal center position of the dinosaur
- `y_pos`: Vertical center position of the dinosaur (adjusted +5 pixels)
- `half_y`: Vertical midpoint of the image

#### Methods

**`__init__(self, img_path)`**
- Loads image from file path or BytesIO stream
- Converts image to NumPy array
- Calculates vertical midpoint

**`detect(self)`**
- Defines Region of Interest (ROI): `[half_y-100 : half_y+100, 30:100]`
- Identifies non-white pixels (potential dinosaur pixels)
- Filters for gray pixels with RGB value `[83, 83, 83]` (dinosaur color)
- Calculates center position using mean of all dinosaur pixel coordinates
- Stores center position in `self.x_pos` and `self.y_pos`

#### Algorithm Details
1. Create a binary mask for non-white pixels in the ROI
2. Extract coordinates of all non-white pixels
3. Filter for exact gray color `[83, 83, 83]`
4. Calculate average X and Y positions
5. Apply +5 pixel offset to Y position for better accuracy

---

### 3. ObstacleDetector Class (`detect_obstacles.py`)

**Purpose**: Identifies obstacles (cacti, birds) and calculates optimal jump trigger points.

#### Class Structure

```python
class ObstacleDetector:
    def __init__(self, dino_x, dino_y, img_path)
    def detect(self)
```

#### Attributes
- `np_array`: NumPy array of the screenshot
- `dino_x`, `dino_y`: Dinosaur's current position
- `roi`: Region of Interest `[dino_y-100 : dino_y+5, dino_x+100 : screen_width]`
- `obstacles`: List of detected obstacle positions `[[x, y], ...]`
- `jump_points`: List of trigger points for jumping `[[x-100, y], ...]`
- `min_obstacle_x`, `max_obstacle_x`: Boundaries of obstacle detection zone

#### Methods

**`__init__(self, dino_x, dino_y, img_path)`**
- Initializes detector with dinosaur position
- Defines forward-looking ROI (100 pixels ahead of dinosaur)
- Sets up empty obstacle tracking lists

**`detect(self)`**
- Identifies all non-white pixels in the ROI
- Filters for dark pixels (mean RGB < 150) to exclude ground lines
- Groups obstacles using 150-pixel sliding windows
- Finds the leftmost point of each obstacle
- Calculates jump points (100 pixels before each obstacle)

#### Algorithm Details

**Step 1: Pixel Collection**
- Create binary mask for non-white pixels
- Filter pixels with mean value < 150 (dark obstacles only)
- Store as list of `(y, x, pixel_value)` tuples

**Step 2: Obstacle Grouping**
- Use 150-pixel sliding windows starting from `min_obstacle_x`
- For each window, find the leftmost pixel
- Store as obstacle coordinate `[x, y]`

**Step 3: Jump Point Calculation**
- For each obstacle at position `[x, y]`
- Create jump point at `[x-100, y]` (100 pixels before obstacle)
- This gives the bot enough reaction time to jump

---

## Game Logic Flow

```
1. Capture Screenshot (PNG data in memory)
           ↓
2. Detect Dinosaur Position
   - ROI: Center region [half_y±100, 30:100]
   - Find gray pixels [83,83,83]
   - Calculate center position
           ↓
3. Validate Dinosaur Y-Position
   - If y < 480 or y > 495: Skip (dinosaur is jumping)
   - Prevents mid-air action conflicts
           ↓
4. Detect Obstacles
   - ROI: Forward region [dino_y±100, dino_x+100:end]
   - Find dark pixels (obstacles)
   - Group into distinct obstacles
   - Calculate jump trigger points
           ↓
5. Decision Making
   - Calculate distance: jump_point_x - dino_x
   - If 0 ≤ distance ≤ 250:
       * If obstacle_y < dino_y - 50: Duck (DOWN key)
       * Else: Jump (SPACE key)
           ↓
6. Execute Action
   - Press keyboard key via PyAutoGUI
   - Wait 10ms before next iteration
```

## Key Constants & Thresholds

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Dinosaur Gray Color | `[83, 83, 83]` | Identifies dinosaur pixels |
| Obstacle Detection Threshold | `< 150` (mean RGB) | Filters dark obstacles from ground |
| Y-Position Valid Range | `480-495` pixels | Normal ground position |
| Action Distance Window | `0-250` pixels | Trigger range for jump/duck |
| Duck Threshold | `dino_y - 50` | If obstacle is 50+ pixels above |
| Jump Anticipation | `100` pixels | Jump trigger before obstacle |
| Obstacle Grouping Window | `150` pixels | Groups nearby pixels into one obstacle |
| Loop Delay | `0.01` seconds | 100 FPS detection rate |

## Important Functions

### Main Loop Functions

**Screenshot Capture**
```python
png_data = driver.get_screenshot_as_png()
image_path = BytesIO(png_data)
```
- Captures game state without saving to disk
- Uses in-memory BytesIO stream for speed

**Dinosaur Position Validation**
```python
if dinosaur_y < 480 or dinosaur_y > 495:
    print(f"Skipping detection - dinosaur jumping (y={dinosaur_y})")
    continue
```
- Prevents action spam during jumps
- Ensures clean decision making

**Distance Calculation & Action Trigger**
```python
distance = jump_point[0] - dinosaur_x  
if 0 <= distance <= 250: 
    if jump_point[1] < dinosaur_y - 50:
        pyautogui.press("down")  # Duck for flying obstacles
    else: 
        pyautogui.press('space')  # Jump for ground obstacles
```

## Performance Considerations

- **Real-time Processing**: 10ms loop delay (~100 FPS)
- **Memory Efficient**: Uses BytesIO streams instead of file I/O
- **Optimized ROI**: Only processes relevant image regions
- **Early Exit**: Skips processing when dinosaur is already jumping

## Dependencies

```
selenium
pyautogui
pillow (PIL)
numpy
```

## How to Run

1. Install dependencies:
   ```bash
   pip install selenium pyautogui pillow numpy
   ```

2. Run the bot:
   ```bash
   python3 main.py
   ```

3. The game will automatically start playing!

## Potential Improvements

1. **Adaptive Thresholds**: Dynamically adjust action distance based on game speed
2. **Machine Learning**: Train a neural network to predict optimal jump timing
3. **Speed Detection**: Detect game speed increases and adjust reaction times
4. **Multi-obstacle Handling**: Better handling of consecutive obstacles
5. **Error Recovery**: Auto-restart on game over

## Troubleshooting

**Bot doesn't jump in time**
- Increase the action distance window (currently 250 pixels)
- Reduce the jump anticipation offset (currently 100 pixels)

**Bot jumps too early**
- Decrease the action distance window
- Increase the jump anticipation offset

**Dinosaur not detected**
- Verify the gray color value matches your screen: `[83, 83, 83]`
- Check the ROI boundaries match your screen resolution

**Obstacles not detected**
- Adjust the dark pixel threshold (currently < 150)
- Verify obstacles are within the forward-looking ROI
