from typing import List, Tuple, Generator, Set
from itertools import chain

import numpy as np

from gym_maze.common import MAZE_PATH, MAZE_WALL
from gym_maze.common.maze_utils import adjacent_cell_values


def get_all_transitions(matrix: np.ndarray) -> List[Tuple[List, int, List]]:
    """
    Returns list of tuples:
    (perception, action, perception)
    """
    transitions = []

    north = np.copy(matrix)
    west = np.rot90(np.copy(north))
    south = np.rot90(np.copy(west))
    east = np.rot90(np.copy(south))

    directions = [north, west, south, east]

    # Get all step transitions
    steps = list(
        chain.from_iterable(_get_step_transitions(d) for d in directions))

    # Get all left/right rotation transitions
    rotations = list(
        chain.from_iterable(_get_rotation_transitions(d) for d in directions))

    transitions.extend(steps)
    transitions.extend(rotations)

    return [(p0.tolist(), a, p1.tolist()) for (p0, a, p1) in transitions]


def _get_step_transitions(matrix: np.ndarray) -> Generator:
    for path_cell in zip(*np.where(matrix == MAZE_PATH)):
        p0 = np.array(adjacent_cell_values(matrix, *path_cell), dtype=np.uint8)

        next_cell = (path_cell[0] - 1, path_cell[1])
        if matrix[next_cell] != MAZE_WALL:
            p1 = np.array(adjacent_cell_values(matrix, *next_cell), dtype=np.uint8)
            yield p0, 0, p1
        else:
            yield p0, 0, p0


def _get_rotation_transitions(matrix: np.ndarray) -> Generator:
    for path_cell in zip(*np.where(matrix == MAZE_PATH)):
        p0 = np.array(adjacent_cell_values(matrix, *path_cell), dtype=np.uint8)

        yield p0, 1, np.roll(p0, 2)  # perception of turning left
        yield p0, 2, np.roll(p0, -2)  # perception of turning right