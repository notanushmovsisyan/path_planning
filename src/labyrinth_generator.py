import random

S, E = 1, 2  # Direction constants


class State:
    def __init__(self, width, next_set=-1):
        self.width = width
        self.next_set = next_set
        self.sets = {}
        self.cells = {}

    def next(self):
        return State(self.width, self.next_set)

    def populate(self):
        for cell in range(self.width):
            if cell not in self.cells:
                self.next_set += 1
                self.sets[self.next_set] = [cell]
                self.cells[cell] = self.next_set
        return self

    def merge(self, sink_cell, target_cell):
        sink = self.cells[sink_cell]
        target = self.cells[target_cell]
        self.sets[sink].extend(self.sets[target])
        for cell in self.sets[target]:
            self.cells[cell] = sink
        del self.sets[target]

    def same(self, cell1, cell2):
        return self.cells[cell1] == self.cells[cell2]

    def add(self, cell, set_id):
        self.cells[cell] = set_id
        if set_id not in self.sets:
            self.sets[set_id] = []
        self.sets[set_id].append(cell)

    def each_set(self):
        return list(self.sets.items())


def step(state, finish=False):
    connected_sets = []
    connected_set = [0]

    for c in range(state.width - 1):
        if state.same(c, c + 1) or (not finish and random.randint(0, 1)):
            connected_sets.append(connected_set)
            connected_set = [c + 1]
        else:
            state.merge(c, c + 1)
            connected_set.append(c + 1)

    connected_sets.append(connected_set)

    verticals = []
    next_state = state.next()

    if not finish:
        for set_id, members in state.each_set():
            chosen = random.sample(members, k=random.randint(1, len(members)))
            verticals.extend(chosen)
            for cell in chosen:
                next_state.add(cell, set_id)

    row = []
    for connected_set in connected_sets:
        for i, cell in enumerate(connected_set):
            last = (i + 1 == len(connected_set))
            mask = 0 if last else E
            if cell in verticals:
                mask |= S
            row.append(mask)

    return next_state.populate(), row


def generate(width, height, seed=None):
    if seed is None:
        seed = random.randint(0, 0xFFFFFFFF)
    random.seed(seed)

    state = State(width).populate()
    graph = {}

    for row_idx in range(height):
        state, row = step(state)
        for col_idx, cell in enumerate(row):
            node = (row_idx, col_idx)
            graph[node] = []

            if cell & E:
                graph[node].append((row_idx, col_idx + 1))
            if cell & S:
                graph[node].append((row_idx + 1, col_idx))

    # Final row
    state, row = step(state, finish=True)
    for col_idx, cell in enumerate(row):
        node = (height, col_idx)
        graph[node] = []

        if cell & E:
            graph[node].append((height, col_idx + 1))

    return graph, seed


def print_labyrinth(graph, width, height):
    maze_rows = 2 * height + 1
    maze_cols = 2 * width + 1
    maze = [['█'] * maze_cols for _ in range(maze_rows)]

    for y in range(height):
        for x in range(width):
            cell = (y, x)
            cell_row, cell_col = 2 * y + 1, 2 * x + 1
            maze[cell_row][cell_col] = ' '  # Cell itself

            for ny, nx in graph.get(cell, []):
                if ny == y and nx == x + 1:  # right
                    maze[cell_row][cell_col + 1] = ' '
                elif ny == y and nx == x - 1:  # left
                    maze[cell_row][cell_col - 1] = ' '
                elif ny == y + 1 and nx == x:  # down
                    maze[cell_row + 1][cell_col] = ' '
                elif ny == y - 1 and nx == x:  # up
                    maze[cell_row - 1][cell_col] = ' '

    # Add entrance and exit
    maze[1][0] = ' '  # entrance
    maze[2 * height - 1][2 * width] = ' '  # exit

    for row in maze:
        print("".join(row))
    print()


def print_labyrinth_binary(graph, width, height):
    maze_rows = 2 * height + 1
    maze_cols = 2 * width + 1
    maze = [[1] * maze_cols for _ in range(maze_rows)]

    for y in range(height):
        for x in range(width):
            cell = (y, x)
            cell_row, cell_col = 2 * y + 1, 2 * x + 1
            maze[cell_row][cell_col] = 0

            for ny, nx in graph.get(cell, []):
                if ny == y and nx == x + 1:
                    maze[cell_row][cell_col + 1] = 0
                elif ny == y and nx == x - 1:
                    maze[cell_row][cell_col - 1] = 0
                elif ny == y + 1 and nx == x:
                    maze[cell_row + 1][cell_col] = 0
                elif ny == y - 1 and nx == x:
                    maze[cell_row - 1][cell_col] = 0

    maze[1][0] = 0
    maze[2 * height - 1][2 * width] = 0

    for row in maze:
        print("".join(str(c) for c in row))
    print()
