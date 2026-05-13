import cv2
import random
import numpy as np

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

class Fruit:
    def __init__(self, screen_width, screen_height, fruit_img, half_img):
        self.x = random.randint(100, screen_width - 100)
        self.speed_x = random.randint(-4, 4)   
        
        # --- NEW: Randomly pick spawn mode ---
        self.spawn_mode = random.choice(["bottom", "top"])
        
        if self.spawn_mode == "bottom":
            # Original Logic: Shoot up from the bottom
            self.y = screen_height - 10
            self.speed_y = -random.randint(18, 28) 
            self.gravity = 0.8
        else:
            # New Logic: Drop from the top
            self.y = -80 # Start cleanly above the screen
            self.speed_y = random.randint(2, 6) # Give it a slight initial downward push
            # We use lower gravity for top drops so they don't zoom past too quickly!
            self.gravity = 0.4 
            
        # Store the images
        self.img = fruit_img
        self.half_left = half_img
        self.half_right = cv2.flip(half_img, 1) 
        
        h, w = self.img.shape[:2]
        self.radius = max(w, h) // 2 
        
        self.is_sliced = False
        self.sliced_timer = 0 

    def update(self):
        self.speed_y += self.gravity
        self.x += self.speed_x
        self.y += self.speed_y
        
        if self.is_sliced:
            self.sliced_timer += 1

    def draw(self, frame):
        if not self.is_sliced:
            top_left_x = int(self.x - self.radius)
            top_left_y = int(self.y - self.radius)
            draw_transparent(frame, self.img, top_left_x, top_left_y)
        else:
            offset_x = self.sliced_timer * 6  
            offset_y = self.sliced_timer * 3  
            
            left_x = int(self.x - self.radius - offset_x)
            left_y = int(self.y - self.radius + offset_y)
            
            right_x = int(self.x + offset_x)
            right_y = int(self.y - self.radius + offset_y)
            
            draw_transparent(frame, self.half_left, left_x, left_y)
            draw_transparent(frame, self.half_right, right_x, right_y)