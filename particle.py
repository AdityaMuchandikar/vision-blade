import cv2
import random
import math

class Particle:
    def __init__(self, x, y, color=(150, 240, 255)):
        self.x = x
        self.y = y
        self.vx = random.uniform(-12, 12)
        self.vy = random.uniform(-15, -2)
        self.gravity = 0.8
        self.radius = random.randint(3, 9)
        self.color = color 
        self.lifetime = random.randint(15, 35) 
        self.max_lifetime = self.lifetime

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, frame):
        if self.lifetime > 0:
            current_radius = max(1, int(self.radius * (self.lifetime / self.max_lifetime)))
            cv2.circle(frame, (int(self.x), int(self.y)), current_radius, self.color, -1)

# --- NEW: BOMB EXPLOSION PARTICLE ---
class ExplosionParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # Shoot outward in a 360 degree circle
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(5, 25) # Highly explosive speed!
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        self.gravity = 0.1 # Very low gravity so it acts like floating smoke
        self.radius = random.randint(5, 15)
        
        # Pick a random fire/smoke color (BGR format)
        # Colors: Orange, Red, Yellow, Dark Gray, Light Gray
        colors = [(0, 165, 255), (0, 0, 255), (0, 255, 255), (50, 50, 50), (150, 150, 150)]
        self.color = random.choice(colors)
        
        self.lifetime = random.randint(20, 40)
        self.max_lifetime = self.lifetime

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, frame):
        if self.lifetime > 0:
            current_radius = max(1, int(self.radius * (self.lifetime / self.max_lifetime)))
            cv2.circle(frame, (int(self.x), int(self.y)), current_radius, self.color, -1)