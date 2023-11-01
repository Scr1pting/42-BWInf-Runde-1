import re

from path import find_fastest_path
from map_render import render_path


def split_list_at_empty_elements(input_list: list) -> list:
    """Splits a list into into a more dimensional list at an empty elements, like [].

    Args:
        input_list (list): input list

    Returns:
        list: splitted list
    """
    result = []
    sub_list = []

    # Iterate ove input list
    for item in input_list:
        # If item is empty, add it the sublist to the result
        if not item:
            if sub_list:  # Avoid adding empty sublists when two elements are empty
                result.append(sub_list)
            sub_list = []  # Start a new sublist
        else:
            # Otherwise add the element to the sublist
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

    return None # Return None if the element is not found in the list


def start_command_line_interface():
    """Starts command line interface asking user for path to blueprint, save path, and render mode.
    Saves guide.
    """
    # Prompt user for path to blueprint and save path
    path_to_blueprint = input("Path to blueprint: " )
    save_path = input("Path to save guide: ")

    # Continuously ask user how to render the path (as characters or as lines) until
    # they enter a valid input
    while True:
        render_question = input("Render path as characters or as lines (1/2/?): ")
        if render_question.lower() in ["1", "c", "char", "characters"]:
            render_mode = "characters"
            break
        elif render_question.lower() in ["2", "t", "lines"]:
            render_mode = "lines"
            break
        else:
            print("Lines are easier to follow but may break when using a non-monospace font or line spacing.")

    # Read blueprint file
    with open(path_to_blueprint, "r") as file:
        blueprint_file = file.read()

    # Remove empty lines at the beginning or end
    blueprint_file.strip()

    # Separates levels through empty elements
    # Therefore flat
    flat_blueprint = []

    for line in blueprint_file.splitlines():
        # Remove the initial info provided at the beginning of the files
        if re.search(r"\d+\s\d+", line):
            continue

        # Split the line into individual list elements
        elements = list(line.strip())
        
        # Append the elements as a row to the matrix
        flat_blueprint.append(elements)

    # Split the flat blueprint into levels
    blueprint = split_list_at_empty_elements(flat_blueprint)

    # Find both endpoints
    location_a = find_first_occurrence_3d(blueprint, "A")
    location_b = find_first_occurrence_3d(blueprint, "B")

    # Find fastest path between endpoints
    fastest_path = find_fastest_path(blueprint=blueprint, location_a=location_a, location_b=location_b)

    # Render path
    guide = render_path(blueprint=blueprint, path=fastest_path, render_mode=render_mode)

    # Write path to previously determined file
    with open(save_path, "w") as file:
        file.write(str(guide))


# Check whether main.py runs as main program
if __name__ == "__main__":
    start_command_line_interface()
