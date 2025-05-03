# 🦖 Dinosaur Jump Game (Pygame)

A simple yet fun side-scrolling dinosaur jump game built with Python and Pygame. Inspired by the classic Chrome offline game, this version features running, jumping, ducking, multiple obstacle types (cactus, rock, bird), animated clouds, day/night cycle, increasing difficulty, and persistent high scores.

---

## 🎮 Features

- Smooth animation and controls (jump/duck)
- Three types of obstacles with unique behavior
- Animated birds and clouds
- Day/night cycle based on score progression
- Gradually increasing speed/difficulty
- Pause functionality (ESC)
- Persistent high score saving

---

## 🖥️ Requirements

- Python 3.7+
- [Pygame](https://www.pygame.org/)  
  Install with:
 
  pip install pygame


---

## 🚀 How to Play

1. **Install dependencies**:

   ```bash
   pip install pygame
   ```

2. **Run the game**:

   ```bash
   python main.py
   ```

3. **Controls**:

   * `SPACE`: Jump
   * `DOWN` or `S`: Duck
   * `ESC`: Pause / Exit
   * After game over, press `SPACE` to restart

---

## 🗃️ Project Structure


dino-jump/
│
├── main.py               # Main game code
├── save/
│   └── highscore.txt     # High score saved here
└── README.md             # Game instructions


---

## 🏆 High Score

The high score is automatically saved in a `save/highscore.txt` file. If the directory doesn't exist, it will be created on the first run.

---

## 🛠️ Customization Ideas

* Add sound effects and background music
* Add power-ups or coins
* Implement a menu and settings screen
* Use sprite images instead of Pygame shapes

---

## 📄 License

This project is open-source and available under the MIT License.
Feel free to use or modify it in your own projects.

---

## 🤝 Contributions

Feel free to fork the repo and submit pull requests!
Suggestions, feedback, and bug reports are welcome.

```
