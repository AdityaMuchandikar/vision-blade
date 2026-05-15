# 🗡️ Vision Blade

A real-time, interactive computer vision game built with Python. **Vision Blade** turns your webcam into an arcade interface, allowing you to slice falling fruits and dodge bombs using just your index finger.

Powered by **MediaPipe** for edge-device hand tracking and **OpenCV** for rendering, the engine achieves zero-latency interaction with robust procedural physics and state management.

## ✨ Features
* **Zero-Latency Tracking:** Utilizes MediaPipe's optimized Hand landmark detection to track finger coordinates in real-time.
* **Procedural Physics:** Objects feature randomized spawning parameters, gravity curves, and collision detection using point-to-line shortest distance algorithms.
* **Game State Machine:** Clean architectural separation between `MENU`, `PLAYING`, and `GAME_OVER` states.
* **Dynamic VFX:** Features additive-blending particle systems for juice splatters and bomb explosions that animate independently of the game state.

## 🛠️ Tech Stack
* **Language:** Python 3.10.11
* **Computer Vision:** OpenCV (`cv2`)
* **Machine Learning Tracking:** Google MediaPipe (`mediapipe 0.10.9`)
* **Math & Physics:** `numpy`, `math`

## 🚀 Installation & Setup

1. **Clone the repository:**
2. **Install dependencies:**
   ```bash
   ('requirements.txt')
4. **Run the engine:**
   ```bash
   python main.py

## 🎮 Controls
* Spacebar: Start Game / Play Again
* M: Toggle between Arcade Mode (lives and bombs) and Relaxed Mode (no penalties)
* R: Instant Restart
* Q: Quit Application

## 🏗️ Architecture

The codebase is strictly modularized to separate tracking logic, entity physics, and rendering:

* main.py - The core game loop, state machine, and UI rendering compositor.
* tracker.py - Wraps the MediaPipe API for clean, decoupled coordinate extraction.
* fruit.py & items.py - Object-oriented classes handling gravity, velocity, and state for interactive targets.
* particle.py - Manages the lifecycles of procedural visual effects.

# Built for exploring "MediaPipe" and real-time human-computer interaction.
