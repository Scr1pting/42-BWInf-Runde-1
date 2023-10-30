import re
import itertools

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from tqdm import tqdm

from close_by import get_valid_descents


def render_path(map_top: list, map_bottom: list, path: list) -> str:
    guide = [map_bottom, map_top]

    for index, element in enumerate(path):
        if index == 0 or index == len(path) - 1:
            continue

        next_element = path[index + 1]
        
        level = element[0]
        row = element[1]
        col = element[2]

        if element[0] != next_element[0]:
            guide[level][row][col] = "!"
        elif element[1] > next_element[1]:
            guide[level][row][col] = "v"
        elif element[1] > next_element[1]:
            guide[level][row][col] = "^"
        elif element[2] > next_element[2]:
            guide[level][row][col] = "<"
        elif element[2] < next_element[2]:
            guide[level][row][col] = ">"

    return guide
            

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

def path_between(arr: list, location_a: tuple, location_b: tuple):
    # Get slices between points
    if location_a[0] == location_b[0]:
        sl = arr[location_a[0]][min(location_a[1], location_b[1]) + 1 : max(location_a[1], location_b[1])]
    elif location_a[1] == location_b[1]:
        sl = [row[location_a[0]] for row in arr[min(location_a[0], location_b[0]) + 1 : max(location_a[0], location_b[1])]]
    else:
        return False    

    # Validate slices only contain 1
    return all(x == 1 for x in sl)

def shortest_path_no_obstacles(location_a: tuple, location_b: tuple):
    return abs(location_a[0] - location_b[0]) + abs(location_a[1] - location_b[1])

def find_fastest_path(map_top: list, map_bottom: list, location_a: tuple, location_b: tuple):
    fastest_path = find_path(matrix=map_top, location_a=location_a, location_b=location_b, level=1)
    fastest_path_length = len(fastest_path)

    immediate_bottom = [(1, location_a[0], location_a[1])] + find_path(matrix=map_bottom, location_a=location_a, location_b=location_b, level=0) + [(1, location_b[0], location_b[1])]

    if not fastest_path or (immediate_bottom and len(immediate_bottom) + 4 < len(fastest_path)):
        fastest_path = immediate_bottom
        fastest_path_length = len(immediate_bottom) + 4

    too_far_away_descends_a = []
    too_far_away_descends_b = []
    too_long_descends = []

    valid_descents = get_valid_descents(map_top, map_bottom)

    combinations = list(itertools.combinations(valid_descents, 2))

    for index, combination in enumerate(combinations):
        print(f"{index}/{len(combinations)}", end="\r")

        if combination[0] in too_far_away_descends_a or combination[1] in too_far_away_descends_b:
            continue
        elif combination[0] in too_long_descends and combination[1] in too_long_descends:
            continue
        elif path_between(map_top, location_a, location_b) or path_between(map_top, combination[0], combination[1]):
            continue
        elif shortest_path_no_obstacles(location_a=location_a, location_b=combination[0]) + shortest_path_no_obstacles(location_a=combination[0], location_b=combination[1]) + shortest_path_no_obstacles(location_a=combination[1], location_b=location_b) + 4 >= fastest_path_length:
            continue
        
        path_to_descent = find_path(matrix=map_top, location_a=location_a, location_b=combination[0], level=1)

        if not path_to_descent or len(path_to_descent) + shortest_path_no_obstacles(location_a=combination[0], location_b=location_b) + 6 >= fastest_path_length:
            too_far_away_descends_a.append(combination[0])
            continue

        if len(path_to_descent) + shortest_path_no_obstacles(location_a=combination[0], location_b=combination[1]) + shortest_path_no_obstacles(location_a=combination[1], location_b=location_b) + 4 >= fastest_path_length:
            continue

        path_descent = find_path(matrix=map_bottom, location_a=combination[0], location_b=combination[1], level=0)

        if not path_descent or len(path_descent) + 6 >= fastest_path_length:
            too_long_descends += combination
            continue

        if len(path_to_descent) + len(path_descent) + shortest_path_no_obstacles(combination[1], location_b) + 4 >= fastest_path_length:
            continue

        path_from_descent = find_path(matrix=map_top, location_a=combination[1], location_b=location_b, level=1)

        if not path_from_descent or shortest_path_no_obstacles(location_a=location_a, location_b=combination[1]) + len(path_from_descent) + 6 >= fastest_path_length:
            too_far_away_descends_b.append(combination[1])
            continue

        path = path_to_descent + path_descent + path_from_descent

        if not fastest_path or len(path) + 4 <= fastest_path_length:
            fastest_path = path
            fastest_path_length = len(fastest_path) + 4
    
    return fastest_path

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
