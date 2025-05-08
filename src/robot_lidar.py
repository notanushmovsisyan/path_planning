import random
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from path_finder import *


def simulate_lidar(robot_pos, graph, noise_std=0.1):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
    visible = {}
    for dy, dx in directions:
        ny, nx = robot_pos[0] + dy, robot_pos[1] + dx
        if (ny, nx) in graph.get(robot_pos, []):
            noisy_ny = ny + random.gauss(0, noise_std)
            noisy_nx = nx + random.gauss(0, noise_std)
            visible[(round(noisy_ny), round(noisy_nx))] = True
    return visible


def draw_map(robot_map, robot_pos, width, height):
    img = np.ones((height * 2 + 1, width * 2 + 1), dtype=np.uint8) * 255
    for (y, x), neighbors in robot_map.items():
        ry, rx = 2 * y + 1, 2 * x + 1
        img[ry, rx] = 200
        for ny, nx in neighbors:
            if ny == y and nx == x + 1:
                img[ry, rx + 1] = 200
            elif ny == y and nx == x - 1:
                img[ry, rx - 1] = 200
            elif ny == y + 1 and nx == x:
                img[ry + 1, rx] = 200
            elif ny == y - 1 and nx == x:
                img[ry - 1, rx] = 200

    ry, rx = 2 * robot_pos[0] + 1, 2 * robot_pos[1] + 1
    img[ry, rx] = 0

    plt.imshow(img, cmap='gray')
    plt.title("Robot Exploration")
    plt.pause(0.2)
    plt.clf()


def next_forward(robot_pos, graph):
    for neighbor in graph.get(robot_pos, []):
        if neighbor == (robot_pos[0], robot_pos[1] + 1):
            return neighbor
    return None


def explore_with_lidar(graph, width, height):
    robot_pos = (0, 0)
    goal = (height - 1, width - 1)
    robot_map = {robot_pos: []}
    visited = set([robot_pos])
    frontier = [robot_pos]

    plt.figure()

    while True:
        visible = simulate_lidar(robot_pos, graph)

        for neighbor in visible:
            if neighbor not in robot_map:
                robot_map[neighbor] = []
            if neighbor not in robot_map[robot_pos]:
                robot_map[robot_pos].append(neighbor)
            if robot_pos not in robot_map[neighbor]:
                robot_map[neighbor].append(robot_pos)

            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)

        draw_map(robot_map, robot_pos, width, height)

        next_step = next_forward(robot_pos, robot_map)
        if next_step:
            robot_pos = next_step
            continue 

        if robot_pos == goal:
            print("Reached goal!")
            break

        if not frontier:
            print("No more frontier to explore.")
            break

        reachable_frontier = []

        for target in frontier:
            path = pathfinder_algo(robot_map, robot_pos, target)
            if path:
                reachable_frontier.append((len(path), path, target))

        if reachable_frontier:
            reachable_frontier.sort()
            _, path, target = reachable_frontier[0]
            frontier.remove(target)
            for step in path[1:]:
                robot_pos = step
                draw_map(robot_map, robot_pos, width, height)
                time.sleep(0.1)
        else:
            print("Can't reach any more unexplored area.")
            break

    plt.close()

