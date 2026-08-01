import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
from collections import deque
import time

# -----------------------------
# MAZE DEFINITION
# -----------------------------
MAZE = np.array([
    [0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 1, 0]
])

START = (0, 0)
GOAL  = (7, 7)
ROWS, COLS = MAZE.shape
TIME_LIMIT = 30  # seconds

# -----------------------------
# HELPER
# -----------------------------
def get_neighbors(pos):
    r, c = pos
    result = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
            result.append((nr, nc))
    return result

def bfs_solution():
    queue   = deque([START])
    visited = {START}
    parent  = {}
    while queue:
        cur = queue.popleft()
        if cur == GOAL:
            break
        for nb in get_neighbors(cur):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = cur
                queue.append(nb)
    path, node = [], GOAL
    while node != START:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return []
    path.append(START)
    path.reverse()
    return path

# -----------------------------
# GAME STATE
# -----------------------------
class MazePuzzleGame:
    def __init__(self):
        self.player_pos   = START
        self.path_taken   = [START]
        self.solution     = bfs_solution()
        self.sol_len      = len(self.solution)
        self.start_time   = time.time()
        self.game_over    = False
        self.won          = False
        self.show_hint    = False
        self.hint_steps   = 1          # reveal first N steps of solution
        self.hints_used   = 0
        self.moves        = 0
        self.optimal      = self.sol_len - 1  # optimal move count

        # Build display grid: walls=dark, paths=light
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.fig.patch.set_facecolor('#1a1a2e')
        self.fig.canvas.manager.set_window_title("Maze Puzzle - Find the Path!")

        self._build_display()
        self.fig.canvas.mpl_connect('key_press_event', self._on_key)
        self.timer_anim = animation.FuncAnimation(
            self.fig, self._tick, interval=500, cache_frame_data=False
        )
        plt.tight_layout()
        plt.show()

    # ---------------------------
    def _build_display(self):
        ax = self.ax
        ax.clear()
        ax.set_facecolor('#0f3460')

        # Draw maze cells
        for r in range(ROWS):
            for c in range(COLS):
                color = '#16213e' if MAZE[r][c] == 1 else '#e0e0e0'
                rect  = plt.Rectangle([c-0.5, r-0.5], 1, 1,
                                      color=color, zorder=1)
                ax.add_patch(rect)

        # Grid lines
        for r in range(ROWS+1):
            ax.axhline(r-0.5, color='#0f3460', lw=1.5, zorder=2)
        for c in range(COLS+1):
            ax.axvline(c-0.5, color='#0f3460', lw=1.5, zorder=2)

        # Hint path
        if self.show_hint and not self.game_over:
            hint_path = self.solution[1:self.hint_steps+1]
            for (r, c) in hint_path:
                rect = plt.Rectangle([c-0.5, r-0.5], 1, 1,
                                     color='#f5a623', alpha=0.45, zorder=3)
                ax.add_patch(rect)

        # Player trail
        for (r, c) in self.path_taken[1:-1]:
            ax.plot(c, r, 's', color='#4fc3f7', markersize=14,
                    alpha=0.4, zorder=4)

        # START marker
        ax.plot(START[1], START[0], '*', color='#ffd700',
                markersize=20, zorder=6, label='Start')

        # GOAL marker
        ax.plot(GOAL[1], GOAL[0], 'D', color='#e94560',
                markersize=16, zorder=6, label='Goal')

        # Player
        pr, pc = self.player_pos
        ax.plot(pc, pr, 'o', color='#00e676', markersize=20,
                zorder=7, label='You')

        # Win/Lose overlay
        if self.game_over:
            msg   = "*** YOU WIN! ***" if self.won else ">>> TIME'S UP! <<<"
            color = '#00e676'       if self.won else '#e94560'
            sub   = (f"Moves: {self.moves}  |  Optimal: {self.optimal}  |  Hints: {self.hints_used}"
                     if self.won else "Press R to restart")
            ax.text(3.5, 3.5, msg, fontsize=28, fontweight='bold',
                    color=color, ha='center', va='center', zorder=10,
                    bbox=dict(boxstyle='round,pad=0.6', facecolor='#1a1a2e',
                              edgecolor=color, linewidth=3))
            ax.text(3.5, 4.4, sub, fontsize=12, color='white',
                    ha='center', va='center', zorder=10)
            # Show solution
            sx = [p[1] for p in self.solution]
            sy = [p[0] for p in self.solution]
            ax.plot(sx, sy, '--', color='#f5a623', lw=2,
                    alpha=0.7, zorder=5, label='Solution')

        ax.set_xlim(-0.5, COLS-0.5)
        ax.set_ylim(-0.5, ROWS-0.5)
        ax.invert_yaxis()
        ax.set_xticks([])
        ax.set_yticks([])

        # Legend
        legend = ax.legend(loc='upper right', fontsize=9,
                           facecolor='#1a1a2e', edgecolor='#4fc3f7',
                           labelcolor='white', framealpha=0.95)

        # HUD
        elapsed  = time.time() - self.start_time
        remain   = max(0, TIME_LIMIT - elapsed)
        bar_fill = '█' * int(remain / TIME_LIMIT * 20)
        bar_emp  = '░' * (20 - len(bar_fill))
        t_color  = '#e94560' if remain < 10 else '#00e676'

        hud = (f"  Time: {remain:.1f}s  [{bar_fill}{bar_emp}]   "
               f"Moves: {self.moves}   Hints Used: {self.hints_used}\n"
               f"  Arrow keys / WASD -> move   |   H -> hint   |   R -> restart")

        self.ax.set_title(hud, fontsize=10, color=t_color,
                          fontfamily='monospace',
                          fontweight='bold',
                          loc='left', pad=8,
                          backgroundcolor='#1a1a2e')

        self.fig.canvas.draw_idle()

    # ---------------------------
    def _tick(self, frame):
        if self.game_over:
            return
        elapsed = time.time() - self.start_time
        if elapsed >= TIME_LIMIT:
            self.game_over = True
            self.won       = False
            # Reveal solution after losing
            self.show_hint = True
            self.hint_steps = len(self.solution)
        self._build_display()

    # ---------------------------
    def _on_key(self, event):
        if self.game_over:
            if event.key == 'r':
                self._restart()
            return

        key_map = {
            'up':    (-1, 0), 'w': (-1, 0),
            'down':  ( 1, 0), 's': ( 1, 0),
            'left':  ( 0,-1), 'a': ( 0,-1),
            'right': ( 0, 1), 'd': ( 0, 1),
        }

        if event.key in key_map:
            dr, dc   = key_map[event.key]
            r, c     = self.player_pos
            nr, nc   = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
                self.player_pos = (nr, nc)
                self.path_taken.append(self.player_pos)
                self.moves += 1
                if self.player_pos == GOAL:
                    self.game_over = True
                    self.won       = True
                    self.show_hint = True
                    self.hint_steps = len(self.solution)
            self._build_display()

        elif event.key == 'h':
            self.show_hint   = True
            self.hint_steps  = min(self.hint_steps + 2, self.sol_len - 1)
            self.hints_used += 1
            self._build_display()

        elif event.key == 'r':
            self._restart()

    # ---------------------------
    def _restart(self):
        self.player_pos  = START
        self.path_taken  = [START]
        self.start_time  = time.time()
        self.game_over   = False
        self.won         = False
        self.show_hint   = False
        self.hint_steps  = 1
        self.hints_used  = 0
        self.moves       = 0
        self._build_display()

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("  MAZE PUZZLE GAME")
    print("=" * 50)
    print("  Arrow keys or WASD  -> Move")
    print("  H                   -> Reveal hint (costs points)")
    print("  R                   -> Restart")
    print(f"  Time limit          -> {TIME_LIMIT} seconds")
    print("  Reach the red goal before time runs out!")
    print("=" * 50)
    MazePuzzleGame()
