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


def pathfinder_algo(graph, start, end):
    open_list = []
    heapq.heappush(open_list, (0, start))
    path = {}
    g_score = {start: 0}
    f_score = {start: h_score(start, end)}
    closed_set  = set()

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node in closed_set:
            continue

        if current_node == end:
            return reconstruct_path(path, current_node)
        
        closed_set.add(current_node)

        for neighbor in graph.get(current_node, []):
            if neighbor in closed_set:
                continue

            temp_g = g_score[current_node] + 1

            if temp_g < g_score.get(neighbor, float('inf')):
                path[neighbor] = current_node
                g_score[neighbor] = temp_g
                f = temp_g + h_score(neighbor, end)
                f_score[neighbor] = f
                heapq.heappush(open_list, (f, neighbor))

    return None


def test_pathfinder():
    width, height = 10, 6
    graph, _ = generate(width, height)
    path = pathfinder_algo(graph, (0, 0), (height - 1, width - 1))

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
