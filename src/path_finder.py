from labyrinth_generator import *
import heapq


def h_score(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(path, current):
    final_path = [current]
    while current in path:
        current = path[current]
        final_path.append(current)
    return final_path[::-1]


def pathfinder_algo(graph, width, height):
    start_node = (0, 0)
    end_node = (height - 1, width - 1)
    open_list = []
    heapq.heappush(open_list, (0, start_node))
    path = {}
    g_score = {start_node: 0}
    # estimate of distance from final node
    f_score = {start_node: h_score(start_node, end_node)}

    while open_list:
        priority, current_node = heapq.heappop(open_list)

        if current_node == end_node:
            return reconstruct_path(path, current_node)

        for neighbor in graph.get(current_node, []):
            temp_g = g_score[current_node] + 1

            if temp_g < g_score.get(neighbor, float('inf')):
                path[neighbor] = current_node
                g_score[neighbor] = temp_g
                f = temp_g + h_score(neighbor, end_node)
                f_score[neighbor] = f
                heapq.heappush(open_list, (f, neighbor))

    return None


def test_pathfinder():
    width, height = 10, 6
    graph, seed = generate(width, height)
    path = pathfinder_algo(graph, width, height)

    if path is None:
        raise ValueError("No path found!")

    if path[0] != (0, 0):
        raise ValueError("Path does not start at entrance!")

    if path[-1] != (height - 1, width - 1):
        raise ValueError("Path does not end at exit!")

    print("✓ A* pathfinding test passed.")
    print_path_on_maze(graph, path, width, height)


if __name__ == "__main__":
    test_pathfinder()
