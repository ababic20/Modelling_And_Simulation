import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Function to generate an empty grid (all dead cells)
def generate_empty_grid(rows, cols):
    return np.zeros((rows, cols), dtype=int)

def update_grid(grid):
    rows, cols = grid.shape
    new_grid = np.zeros((rows, cols), dtype=int)

    for i in range(rows):
        for j in range(cols):
            # Count alive neighbors with periodic boundary conditions
            live_neighbors = (grid[(i-1)%rows, (j-1)%cols] + grid[(i-1)%rows, j] + grid[(i-1)%rows, (j+1)%cols] +
                              grid[i, (j-1)%cols] + grid[i, (j+1)%cols] +
                              grid[(i+1)%rows, (j-1)%cols] + grid[(i+1)%rows, j] + grid[(i+1)%rows, (j+1)%cols])

            # Apply Game of Life rules
            if grid[i, j] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[i, j] = 0  # Cell dies
                else:
                    new_grid[i, j] = 1  # Cell stays alive
            elif grid[i, j] == 0 and live_neighbors == 3:
                new_grid[i, j] = 1  # Cell becomes alive

    return new_grid

# Function to handle mouse clicks on the grid
def onclick(event):
    # Get the indices of the clicked cell
    if event.xdata is not None and event.ydata is not None:  # Check if within bounds
        col = int(event.xdata)
        row = int(event.ydata)

        # Toggle the cell state (0 or 1)
        if grid[row, col] == 1:
            grid[row, col] = 0  # Make the cell dead
        else:
            grid[row, col] = 1  # Make the cell alive

        # Immediately update the display by setting the new grid data
        img.set_array(grid)
        fig.canvas.draw()

rows, cols = 30, 50

grid = generate_empty_grid(rows, cols)

fig, ax = plt.subplots(figsize=(10, 5))
img = ax.imshow(grid, cmap='Greens', interpolation='nearest', vmin=0, vmax=1)

ax.set_xticks(np.arange(-.5, cols, 1), minor=True)
ax.set_yticks(np.arange(-.5, rows, 1), minor=True)
ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
ax.set_title('Click to select live cells, then close to start the simulation')

# Connect the click event to the grid
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
img = ax.imshow(grid, cmap='Greens', interpolation='nearest', vmin=0, vmax=1)

ax.set_xticks(np.arange(-.5, cols, 1), minor=True)
ax.set_yticks(np.arange(-.5, rows, 1), minor=True)
ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
ax.set_title('Game of Life - Simulation')

def update(frame):
    global grid
    grid = update_grid(grid)
    img.set_array(grid)
    return [img]

ani = FuncAnimation(fig, update, frames=100, interval=200, blit=True)
plt.show()
