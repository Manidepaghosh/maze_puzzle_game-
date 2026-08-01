# 🧩 Maze Puzzle Game

An interactive, dark-themed 2D grid maze game built in **Python** using **Matplotlib** and **NumPy**. Test your problem-solving skills under a 30-second countdown timer, use the BFS-powered hint system when stuck, and compare your moves against the algorithmically calculated optimal path!

---

## 🌟 Key Features

- 🎮 **Interactive Gameplay:** Smooth player navigation using Arrow keys or `WASD`.
- 🧠 **BFS Pathfinding Solver:** Built-in Breadth-First Search algorithm calculates the exact optimal solution path.
- ⏱️ **Countdown Timer HUD:** Real-time animated timer bar (30-second time limit).
- 💡 **Dynamic Hint System:** Press `H` to incrementally reveal steps along the optimal solution path.
- 📊 **Move & Performance Metrics:** Tracks your move count and compares it against the optimal solution length.
- 🎨 **Dark-Mode Visuals:** Customized Matplotlib UI with player trail visualization, goal markers, and status HUD.

---

## 🛠️ Requirements

- Python 3.x
- `numpy`
- `matplotlib`

Install dependencies via pip:
```bash
pip install numpy matplotlib
```

---

## 🚀 How to Run

Run the game directly with Python:

```bash
python maze_puzzle_game.py
```

---

## 🕹️ Controls

| Key | Action |
| --- | --- |
| `W` / `Up Arrow` | Move Up |
| `S` / `Down Arrow` | Move Down |
| `A` / `Left Arrow` | Move Left |
| `D` / `Right Arrow` | Move Right |
| `H` | Reveal next hint step along solution |
| `R` | Restart game |
