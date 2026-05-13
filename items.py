import cv2
import random
import numpy as np

# We include the helper function here so items can draw themselves
def draw_transparent(background, overlay, x, y):
    """Safely draws a PNG with transparency onto a background."""
    bg_h, bg_w = background.shape[:2]
    h, w = overlay.shape[:2]

    y1, y2 = max(0, y), min(bg_h, y + h)
    x1, x2 = max(0, x), min(bg_w, x + w)

    y1o, y2o = max(0, -y), min(h, h - (y + h - bg_h))
    x1o, x2o = max(0, -x), min(w, w - (x + w - bg_w))

    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return background

    overlay_image = overlay[y1o:y2o, x1o:x2o]
    alpha = overlay_image[:, :, 3] / 255.0

    for c in range(3):
        background[y1:y2, x1:x2, c] = (alpha * overlay_image[:, :, c] +
                                      (1 - alpha) * background[y1:y2, x1:x2, c])
    return background

class Bomb:
    def __init__(self, screen_width, screen_height, bomb_img):
        self.x = random.randint(100, screen_width - 100)
        self.speed_x = random.randint(-4, 4)   
        
        # Bombs also randomly drop from the top or shoot from the bottom
        self.spawn_mode = random.choice(["bottom", "top"])
        
        if self.spawn_mode == "bottom":
            self.y = screen_height - 10
            self.speed_y = -random.randint(18, 28) 
            self.gravity = 0.8
        else:
            self.y = -80 
            self.speed_y = random.randint(2, 6) 
            self.gravity = 0.4 
            
        self.img = bomb_img
        h, w = self.img.shape[:2]
        
        # We subtract 5 from the radius to make the bomb's "hitbox" slightly smaller.
        # This makes the game feel more fair and prevents accidental cheap deaths!
        self.radius = (max(w, h) // 2) - 5 
        
        self.is_sliced = False

    def update(self):
        self.speed_y += self.gravity
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, frame):
        # Center the image on the coordinates
        top_left_x = int(self.x - self.radius)
        top_left_y = int(self.y - self.radius)
        draw_transparent(frame, self.img, top_left_x, top_left_y)