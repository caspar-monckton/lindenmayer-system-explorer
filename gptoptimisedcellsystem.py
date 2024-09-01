from typing import Tuple, List, Dict
import numpy as np


def wild_match(matchee: Tuple[int], matcher: Tuple[int]) -> Tuple[bool, List[bool]]:
    match_result = True
    match_positions = [False] * len(matchee)

    for i, (m, c) in enumerate(zip(matchee, matcher)):
        if m != c and c:
            match_result = False

        if m != c and not c:
            match_positions[i] = True

    return match_result, match_positions


class Cell:
    def __init__(self, rules: Dict[Tuple[str], Tuple[str]], state: str) -> None:
        self.state = state
        self.rules = rules

    def set_state(self, state: str) -> None:
        self.state = state

    def get_rules(self) -> Dict[Tuple[str], Tuple[str]]:
        return self.rules

    def set_rules(self, rules: Dict[Tuple[str], Tuple[str]]):
        self.rules = rules

    def get_state(self) -> str:
        return self.state

    def __str__(self) -> str:
        return f"|{self.state}|"

    def __repr__(self) -> str:
        return f"|{self.state}|"


class Grid:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.cells = [[Cell({}, "") for _ in range(width)] for _ in range(height)]

    def get_cells(self):
        return self.cells

    def set_cell_state(self, x: int, y: int, state: str):
        self.cells[y][x].set_state(state)

    def set_cell_rule(self, x: int, y: int, rules: Dict[Tuple[str], Tuple[str]]):
        self.cells[y][x].set_rules(rules)

    def add_cell_rule(self, x: int, y: int, rule: Tuple[Tuple[str], Tuple[str]]):
        rules = self.cells[y][x].get_rules()
        rules[rule[0]] = rule[1]

    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]

    def get_cell_neighbours(self, x: int, y: int) -> Tuple[Cell]:
        positions = [(j - 1, i - 1) for i in range(3) for j in range(3)]
        out = [self.cells[pos[1] + y][pos[0] + x] for pos in positions]
        return tuple(out)

    def insert_cell(self, cell: Cell, x: int, y: int, insertion_index: int):
        cases = [
            (np.transpose, y, slice(1, None), slice(None, -1)),
            (lambda x: x, x, slice(1, None), slice(None, -1)),
            (lambda grid: grid[y][x].set_state(cell.get_state()), 0, None, None),
            (lambda x: x, y, slice(None, -1), slice(1, None)),
            (np.transpose, y, slice(None, -1), slice(1, None)),
        ]

        transpose = np.transpose(np.array(self.cells)).tolist()

        transpose[x].insert(y + insertion_index, cell)
        cases[insertion_index][0](transpose[x])[
            cases[insertion_index][2]
        ] = cell.get_state()

        self.cells = np.transpose(np.array(transpose)).tolist()

    def update_cell(self, x: int, y: int, neighbours: Tuple[Cell]):
        current_cell = self.cells[y][x]
        neighbour_states = tuple([neighbour.get_state() for neighbour in neighbours])
        rules = current_cell.get_rules()

        if neighbour_states in rules:
            for index, cell_to_insert in enumerate(rules[neighbour_states]):
                if cell_to_insert:
                    self.insert_cell(
                        Cell(current_cell.get_rules(), cell_to_insert), x, y, index
                    )
        else:
            key = [i for i in range(9)]
            for rule, result_cell in rules.items():
                match_stats = wild_match(neighbour_states, rule)
                if match_stats[0]:
                    key = tuple(
                        [int(not match_stats[1][i]) * rule[i] for i in range(9)]
                    )
                    for index, cell_to_insert in enumerate(result_cell):
                        if cell_to_insert:
                            self.insert_cell(
                                Cell(current_cell.get_rules(), cell_to_insert),
                                x,
                                y,
                                index,
                            )
                    break

    def update_cells(self, startx: int, starty: int, endx: int, endy: int):
        # 2-ples, first element cell coords, second its neighbour
        updaters = [
            ((x + startx, y + starty), self.get_cell_neighbours(x, y))
            for y, cell_row in enumerate(self.cells[starty:endy])
            for x, _ in enumerate(cell_row[startx:endx])
            if self.cells[y + starty][x + startx].get_rules()
        ]

        for pair in updaters:
            self.cells[pair[0][1]][pair[0][0]]
            self.update_cell(pair[0][0], pair[0][1], pair[1])

    def insert_cell(self, cell: Cell, x: int, y: int, insertion_index: int):
        match (insertion_index):
            case 0:
                transpose = np.transpose(np.array(self.cells)).tolist()
                transpose[x].insert(y, cell)
                transpose[x] = transpose[x][1:]
                self.cells = np.transpose(np.array(transpose)).tolist()
            case 1:
                self.cells[y].insert(x, cell)
                self.cells[y] = self.cells[y][1:]
            case 2:
                self.cells[y][x].set_state(cell.get_state())
            case 3:
                self.cells[y].insert(x + 1, cell)
                self.cells[y] = self.cells[y][:-1]
            case 4:
                transpose = np.transpose(np.array(self.cells)).tolist()
                transpose[x].insert(y + 1, cell)
                transpose[x] = transpose[x][:-1]
                self.cells = np.transpose(np.array(transpose)).tolist()
