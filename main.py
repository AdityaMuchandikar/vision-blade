import cv2
import random
import math
import numpy as np
from tracker import HandTracker
from fruit import Fruit
from particle import Particle, ExplosionParticle # <--- IMPORTED EXPLOSION
from items import Bomb

def point_line_distance(px, py, x1, y1, x2, y2):
    line_mag = math.hypot(x2 - x1, y2 - y1)
    if line_mag == 0:
        return math.hypot(px - x1, py - y1)
        
    u = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_mag ** 2)
    if u < 0.0 or u > 1.0:
        dist1 = math.hypot(px - x1, py - y1)
        dist2 = math.hypot(px - x2, py - y2)
        return min(dist1, dist2)
    
    ix = x1 + u * (x2 - x1)
    iy = y1 + u * (y2 - y1)
    return math.hypot(px - ix, py - iy)

def draw_shadow_text(img, text, pos, font_scale, color, thickness=2, font=cv2.FONT_HERSHEY_DUPLEX):
    cv2.putText(img, text, (pos[0] + 3, pos[1] + 3), font, font_scale, (0, 0, 0), thickness + 3)
    cv2.putText(img, text, pos, font, font_scale, color, thickness)

def draw_transparent_footer(img, w, h):
    overlay = img.copy()
    cv2.rectangle(overlay, (0, h - 50), (w, h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    
    fruits = []
    particles = []
    bombs = [] 
    blade_trail = [] 
    
    game_state = "MENU" 
    score = 0
    lives = 3
    relaxed_mode = False 
    
    # LOAD ASSETS
    bg_image = cv2.imread("assets/background.jpg") 
    apple_img = cv2.imread("assets/apple.png", cv2.IMREAD_UNCHANGED)
    apple_img = cv2.resize(apple_img, (80, 80)) 
    half_apple_img = cv2.imread("assets/half_apple.png", cv2.IMREAD_UNCHANGED)
    half_apple_img = cv2.resize(half_apple_img, (40, 80)) 
    bomb_img = cv2.imread("assets/bomb.png", cv2.IMREAD_UNCHANGED)
    bomb_img = cv2.resize(bomb_img, (90, 90)) 
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        display_frame = cv2.resize(bg_image, (w, h))
        
        _ = tracker.find_hands(img, draw=False) 
        idx_pos = tracker.get_index_tip(img)
        
        if idx_pos:
            blade_trail.append(idx_pos)
            if len(blade_trail) > 8: 
                blade_trail.pop(0)
        else:
            blade_trail.clear() 
            
        if len(blade_trail) > 1:
            for i in range(1, len(blade_trail)):
                thickness = int(i * 1.5)
                cv2.line(display_frame, blade_trail[i-1], blade_trail[i], (0, 255, 255), thickness) 
                cv2.line(display_frame, blade_trail[i-1], blade_trail[i], (255, 255, 255), max(1, thickness-3)) 

        # ==========================================
        # STATE 1: MAIN MENU
        # ==========================================
        if game_state == "MENU":
            draw_shadow_text(display_frame, "Vision Blade", (w//2 - 240, h//2 - 60), 2.5, (0, 255, 255), 5)
            draw_shadow_text(display_frame, "Slice apples. Avoid the bombs!", (w//2 - 230, h//2 + 20), 0.8, (255, 255, 255), 1)
            draw_shadow_text(display_frame, "Press [SPACE] to Start", (w//2 - 180, h//2 + 100), 1.2, (0, 255, 0), 2)

        # ==========================================
        # STATE 2: PLAYING
        # ==========================================
        elif game_state == "PLAYING":
            if random.randint(1, 35) == 1:
                fruits.append(Fruit(w, h, apple_img, half_apple_img))
                
            if random.randint(1, 100) == 1:
                bombs.append(Bomb(w, h, bomb_img))
                
            for f in fruits[:]:
                f.update()
                f.draw(display_frame) 
                
                if not f.is_sliced and len(blade_trail) >= 2:
                    p1 = blade_trail[-2]
                    p2 = blade_trail[-1]
                    dist = point_line_distance(f.x, f.y, p1[0], p1[1], p2[0], p2[1])
                    
                    if dist < f.radius:
                        f.is_sliced = True
                        score += 10
                        for _ in range(15): 
                            particles.append(Particle(f.x, f.y))
                        
                if f.y > h + 100: 
                    if not f.is_sliced and not relaxed_mode:
                        lives -= 1
                        if lives <= 0:
                            game_state = "GAME_OVER"
                    if f in fruits:
                        fruits.remove(f)
                elif f.sliced_timer > 15:
                    if f in fruits:
                        fruits.remove(f)
                        
            for b in bombs[:]:
                b.update()
                b.draw(display_frame)
                
                if len(blade_trail) >= 2 and not relaxed_mode:
                    p1 = blade_trail[-2]
                    p2 = blade_trail[-1]
                    dist = point_line_distance(b.x, b.y, p1[0], p1[1], p2[0], p2[1])
                    
                    if dist < b.radius:
                        # --- NEW: SPAWN BOMB EXPLOSION ---
                        for _ in range(40): # Huge burst!
                            particles.append(ExplosionParticle(b.x, b.y))
                        game_state = "GAME_OVER"
                        
                if b.y > h + 100 and b in bombs:
                    bombs.remove(b)

        # ==========================================
        # STATE 3: GAME OVER
        # ==========================================
        elif game_state == "GAME_OVER":
            draw_shadow_text(display_frame, "GAME OVER", (w//2 - 200, h//2 - 50), 2.5, (0, 0, 255), 5)
            draw_shadow_text(display_frame, f"Final Score: {score}", (w//2 - 130, h//2 + 30), 1.5, (255, 255, 255), 3)
            draw_shadow_text(display_frame, "Press [SPACE] to Play Again", (w//2 - 220, h//2 + 90), 1.0, (0, 255, 255), 2)

        # ==========================================
        # UNIVERSAL RENDERING (Runs in ALL states)
        # ==========================================
        # --- MOVED: PROCESS PARTICLES ---
        # Because this is here, the explosion keeps expanding during the Game Over screen!
        for p in particles[:]:
            p.update()
            p.draw(display_frame)
            if p.lifetime <= 0:
                particles.remove(p)

        draw_shadow_text(display_frame, f"Score: {score}", (30, 50), 1.2, (0, 255, 0), 2)
        
        mode_text = "Relaxed Mode" if relaxed_mode else "Arcade Mode"
        mode_color = (255, 200, 0) if relaxed_mode else (0, 0, 255)
        draw_shadow_text(display_frame, mode_text, (w - 280, 50), 1.0, mode_color, 2)
        
        if not relaxed_mode:
            draw_shadow_text(display_frame, f"Lives: {'X ' * lives}", (w - 280, 90), 1.2, (0, 0, 255), 2)

        draw_transparent_footer(display_frame, w, h)
        controls_text = "CONTROLS: [M] Toggle Mode  |  [R] Restart  |  [Q] Quit"
        draw_shadow_text(display_frame, controls_text, (w//2 - 320, h - 15), 0.7, (200, 200, 200), 1)
        
        cv2.namedWindow("Hand Slicer", cv2.WINDOW_NORMAL)
        cv2.imshow("Hand Slicer", display_frame) 
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m'): 
            relaxed_mode = not relaxed_mode
            if relaxed_mode and game_state == "GAME_OVER":
                game_state = "PLAYING" 
            lives = 3 
        elif key == ord('r'):
            score = 0
            lives = 3
            fruits.clear()
            particles.clear()
            bombs.clear() 
            game_state = "PLAYING"
        elif key == ord(' '): 
            if game_state == "MENU" or game_state == "GAME_OVER":
                score = 0
                lives = 3
                fruits.clear()
                particles.clear()
                bombs.clear() 
                game_state = "PLAYING"

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()