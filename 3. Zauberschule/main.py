import re

from path import find_fastest_path
from map_render import render_path


def split_list_at_empty_elements(input_list: list) -> list[list]:
    result = []
    sub_list = []

    for item in input_list:
        if not item:
            if sub_list:  # Avoid adding empty sublists
                result.append(sub_list)
            sub_list = []  # Start a new sublist
        else:
            sub_list.append(item)

    if sub_list:  # Add the last sublist if not empty
        result.append(sub_list)

    return result

def find_first_occurrence_3d(arr: list, target: any) -> tuple[int, int, int]:
    """Finds the first occurrence of a target element in a 3d list.

    Args:
        arr (list): the 3d list that is searched
        target (any): the searched-for element

    Returns:
        tuple[int, int, int]: the indices of the first occurrence (level, row, column)
    """
    # Iterate over the levels of arr
    for level_index, level in enumerate(arr):
        # Iterate over the rows of arr
        for row_index, row in enumerate(level):
            # Iterate over the contents of each row
            for col_index, value in enumerate(row):
                if value == target:
                    # Return the indices of the first occurrence
                    return level_index, row_index, col_index

    return None # Return None if the element is not found in the array


def start_command_line_interface():
    path_to_blueprint = input("Path to blueprint: " )
    save_path = input("Path to save guide: ")

    while True:
        render_question = input("Render path as characters or as tubes (1/2/?): ")
        if render_question.lower() in ["1", "c", "char", "characters"]:
            render_mode = "characters"
            break
        elif render_question.lower() in ["2", "t", "tubes"]:
            render_mode = "tubes"
            break
        else:
            print("Tubes are easier to follow but may break when using a non-monospace font or line spacing.")

    with open(path_to_blueprint, "r") as file:
        blueprint_file = file.read()

    blueprint_file.strip()

    flat_blueprint = []

    for line in blueprint_file.splitlines():
        if re.search(r"\d+\s\d+", line):
            continue

        elements = list(line.strip())
        
        flat_blueprint.append(elements)

    blueprint = split_list_at_empty_elements(flat_blueprint)

    location_a = find_first_occurrence_3d(blueprint, "A")
    location_b = find_first_occurrence_3d(blueprint, "B")

    fastest_path = find_fastest_path(blueprint=blueprint, location_a=location_a, location_b=location_b)

    guide = render_path(blueprint=blueprint, path=fastest_path, render_mode=render_mode)

    with open(save_path, "w") as file:
        file.write(str(guide))


start_command_line_interface()
