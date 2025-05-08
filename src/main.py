from labyrinth_generator import generate, print_labyrinth
from robot_lidar import explore_with_lidar

if __name__ == "__main__":
    width, height = 10, 6
    graph, seed = generate(width, height)
    print_labyrinth(graph, width, height)
    explore_with_lidar(graph, width, height)

