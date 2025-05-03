# Path Planning
## Eller's Algorithm Maze Generator

This project implements **Eller's Algorithm** for generating random mazes and displays the resulting maze as an ASCII labyrinth. The maze generation is based on **Eller's algorithm**, which is a memory-efficient algorithm that can generate mazes row by row with minimal memory usage. This implementation includes a **graph-based representation** of the maze, which is then visualized as an ASCII maze.

### Features

- **Eller's Algorithm** for maze generation
- **Graph-based maze representation** where each cell and its neighbors are stored as a graph.
- **ASCII Maze Visualization** to print the generated maze in a readable format.
- **Customizable maze dimensions** (width, height, seed).
- **Random seed** generation or user-defined seed for maze consistency.

### How to Use

1. **Generate a maze** by calling the `generate(width, height, seed)` function.
    - **width**: The number of columns in the maze.
    - **height**: The number of rows in the maze.
    - **seed**: Optional. If not provided, a random seed is generated. If you want to reproduce the same maze, you can pass a specific seed.
2. **Visualize the maze** using the `print_labyrinth(graph, width, height)` function to print it in the console.

#### Example Usage

```python
# Generate a maze with width 10 and height 5
graph, used_seed = generate(10, 5)

# Print the maze
print_labyrinth(graph, 10, 5)

```

## The A* Pathfinder Algorithm
This project uses the A* (A-star) algorithm to find the shortest path through the generated maze. A* is a popular and efficient pathfinding algorithm widely used in navigation systems, games, and AI due to its performance and accuracy.

### How to Use

1. Generate a maze as stated in the previous section.
2. **Find the path** by using the `pathfinder_algo(graph, width, height)` function.
    - **graph**: The graph representation of the maze.
    - **width**: The number of columns in the maze.
    - **height**: The number of rows in the maze.
3. **Visualize the maze with the path** with the function `print_path_on_maze(graph, path, width, height)`.

#### Example Usage

```python
#generate a maze with width 10 and height 6
width, height = 10, 6
graph, seed = generate(width, height)

#find path
path = pathfinder_algo(graph, width, height)

#visualize maze and path
print_path_on_maze(graph, path, width, height)

```

