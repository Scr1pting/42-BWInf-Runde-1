import re
import itertools

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from tqdm import tqdm

from close_by import get_valid_descents
from utility import get_surrounding_elements


def split_at_element(arr, element):
  index = arr.index(element) if element in arr else -1

  if index == -1:
    return arr, []
  
  return arr[:index], arr[index + 1:]

def find_first_occurrence(arr: list, target: any) -> tuple:
    """Finds the first occurrence of a target element in a list.

    Args:
        arr (list): the list that is searched
        target (any): the searched-for element

    Returns:
        tuple: the indices of the first occurrence (row, column)
    """
    # Iterate over the rows of arr
    for row_index, row in enumerate(arr):
        # Iterate over the contents of each row
        for col_index, value in enumerate(row):
            if value == target:
                # Return the indices of the first occurrence
                return (row_index, col_index)

    return None # Return None if the element is not found in the array

def find_path(matrix: list, location_a: tuple, location_b: tuple, level: int) -> list:
    if matrix[location_a[0]][location_a[1]] == 0 or matrix[location_b[0]][location_b[1]] == 0:
        return None
    
    grid = Grid(matrix=matrix)

    start = grid.node(location_a[1], location_a[0])
    end = grid.node(location_b[1], location_b[0])

    finder = AStarFinder()

    path_items, _ = finder.find_path(start, end, grid)

    return [(level, path_item.y, path_item.x) for path_item in path_items]


def find_fastest_path(map_top: list, map_bottom: list, location_a: tuple, location_b: tuple):
    fastest_path = find_path(matrix=map_top, location_a=location_a, location_b=location_b, level=1)
    fastest_path_length = len(fastest_path)

    immediate_bottom = [(1, location_a[0], location_a[1])] + find_path(matrix=map_bottom, location_a=location_a, location_b=location_b, level=0) + [(1, location_b[0], location_b[1])]

    if not fastest_path or (immediate_bottom and len(immediate_bottom) + 4 < len(fastest_path)):
        fastest_path = immediate_bottom
        fastest_path_length = len(immediate_bottom) + 4

    updates_fastest_path = 1

    valid_descents = get_valid_descents(map_top, map_bottom)

    combinations = list(itertools.combinations(valid_descents, 2))

    for combination in tqdm(combinations):
        if combination[0] in get_surrounding_elements(map_top, combination[1][0], combination[1][1]):
            continue

        if 
        
        path_to_descent = find_path(matrix=map_top, location_a=location_a, location_b=combination[0], level=1)

        if not path_to_descent or len(path_to_descent) + 6 >= fastest_path_length: continue

        path_descent = find_path(matrix=map_bottom, location_a=combination[0], location_b=combination[1], level=0)

        if not path_descent or len(path_to_descent) + len(path_descent) + 6 >= fastest_path_length:
            continue

        path_from_descent = find_path(matrix=map_top, location_a=combination[1], location_b=location_b, level=1)

        if not path_from_descent: continue

        path = path_to_descent + path_descent + path_from_descent

        if not fastest_path or len(path) + 4 <= fastest_path_length:
            fastest_path = path
            fastest_path_length = len(fastest_path) + 4
    
    return fastest_path

def render_path():
    return 

def main(path: str):
    with open(path, "r") as file:
        blueprint_file = file.read()

    blueprint_file.strip()

    combined_blueprint = []

    for line in blueprint_file.splitlines():
        if re.search(r"\d+\s\d+", line):
            continue

        elements = list(line.strip())
        
        combined_blueprint.append(elements)

    blueprint_top, blueprint_bottom = split_at_element(combined_blueprint, [])

    location_a = find_first_occurrence(blueprint_top, "A")
    location_b = find_first_occurrence(blueprint_top, "B")

    map_top = []
    map_bottom = []

    for row in blueprint_top:
        map_row = []

        for value in row:
            map_row.append(int(re.sub(r"[^0]", "1", str(value).replace("#", "0"))))
        
        map_top.append(map_row)

    for row in blueprint_bottom:
        map_row = []

        for value in row:
            map_row.append(int(re.sub(r"[^0]", "1", str(value).replace("#", "0"))))
        
        map_bottom.append(map_row)

    return find_fastest_path(map_top=map_top, map_bottom=map_bottom, location_a=location_a, location_b=location_b)

print(main(path="example.txt"))
