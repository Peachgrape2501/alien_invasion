# 👾 Alien Invasion — A Python Arcade Shooter

**Alien Invasion** is a fully designed 2D shooter game built in Python using Pygame.  
In this game, you control a spaceship, dodge enemy fire, and shoot down colorful alien fleets with different HP values.  
The game includes sound effects, animations, UI screens, difficulty scaling, and a polished visual theme.

This project is part of my game design portfolio.  
I created all gameplay logic, UI flow, effects, and asset integration myself.

---

<p align="center">
  <img src="images/Alien_Invasion.gif" alt="Alien Invasion Gameplay" width="600">
</p>


## 🎮 Game Features

### 🚀 Player Controls
- Move left and right using **← / →** keys  
- Move using **A / D** keys  
- Fire bullets using **SPACEBAR**

The player ship uses a custom sprite (`player.png`) and smooth movement logic.

---

## 👾 Alien Types & Behavior

There are **three types of aliens**, each with different hit points and score values:

| Alien Color | HP | Score | Special Behavior |
|-------------|----|--------|------------------|
| 🟩 Green     | 1  | 10 pts | Can shoot bullets at the player |
| 🟨 Yellow    | 2  | 20 pts | Moves faster in later rounds |
| 🔴 Red       | 3  | 30 pts | Highest HP, appears less frequently |

Aliens spawn randomly and form a fleet that moves horizontally and descends over time.

---

## 💥 Combat & Effects

### Player Bullet
- Simple energy shot  
- Plays **laser.wav** when fired  

### Enemy Bullet
- Only green aliens shoot  
- Fast downward shot

### Hit Reactions
- Aliens flash white briefly when damaged (**hit effect**)  
- Play **hit.wav** on damage  
- Play **explosion.wav** when dying  
- Small explosion animation plays on death

---

## 📈 Scoring & Difficulty System

- Score increases depending on alien type  
- Highest score is recorded during gameplay  
- Each wave cleared increases:
  - Alien movement speed  
  - Drop speed  
  - Spawn variety  
  - Shooting frequency

A smooth difficulty curve makes later gameplay intense and challenging.

---

## 🖥️ UI & Game Flow

### Start Screen
- Background image: **nightsky.png**
- Custom pixel font: **Pixeled.ttf**
- Tips for controls  
- Styled **Start Game** button  
- Background music: **music.wav**

### In-Game UI
- Lives remaining  
- Score  
- High score display  

### End Screens
- **Game Over** screen  
  - “Game Over (Press ESC)”  
  - Replay button  
  - Exit button

- **Victory Screen**  
  - Triggered when score ≥ 1000  
  - Shows **"YOU WON ⭐"**  
  - Replay & Exit buttons

---

## 🔊 Sound Assets

| File | Usage |
|------|-------|
| `laser.wav` | Player firing |
| `hit.wav` | Alien taking damage |
| `explosion.wav` | Alien death |
| `music.wav` | Background soundtrack |

---

## 📂 Project Structure

```plaintext
alien_invasion/
│
├── alien_invasion.py      # Main game loop and UI flow
├── settings.py            # Game settings and difficulty scaling
├── ship.py                # Player ship logic
├── alien.py               # Alien behavior & drawing
├── bullet.py              # Player bullet
├── enemy_bullet.py        # Enemy bullet
├── explosion.py           # Explosion animation
├── game_stats.py          # Score, high score, lives
├── scoreboard.py          # On-screen score UI
├── button.py              # Reusable button class
│
├── images/                # Player sprite, aliens, UI backgrounds
├── sounds/                # Game sound effects & music
└── fonts/                 # Pixeled.ttf custom pixel font
