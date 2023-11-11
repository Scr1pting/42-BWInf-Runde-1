from utility import get_surrounding_elements
from solve import find_paths, has_path_combination

import random


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

    return None # Return None if the element is not found in the list


def is_solvable_arukone(arukone: list, pairs: int) -> bool:
    """Checks whether an arukone is solvable.

    Note: May take very long to compute as it goes through every possible combination of paths.

    Args:
        arukone (list): a 2d list of the field. Empty squares have a value of 0
        pairs (int): the amount of number pairs

    Returns:
        bool: whether or not an arukone is solvable.
    """
    all_paths = []

    for pair in range(1, pairs + 1):
        # Determine the indices of the first occurrence of a pair
        row, col = find_first_occurrence(arukone, pair)
        # Find paths between the two numbers of the pair
        paths = find_paths(arukone, [(pair, row, col)])
        # Append the paths to all_paths
        all_paths.append(paths)

    # Check whether there is a valid path combination for the arukone
    return has_path_combination(all_paths)


def generate_arukone(field_size: int, pairs: int) -> list:
    """Generates a solvable arukone.

    Args:
        field_size (int): number of rows and columns
        pairs (int): number of pairs

    Raises:
        ValueError: field size too small or not enough pairs

    Returns:
        list: the solvable arukone
    """
    # Raise errors for invalid parameters
    if field_size < 5:
        raise ValueError("Parameter field_size must be greater than 4")
    elif pairs < 2:
        raise ValueError("Parameter pairs must be greater than 2")

    # Generate empty field
    field = [[0 for _ in range(field_size)] for _ in range(field_size)]

    def fill_field(value: int):
        """Randomly fills field with a value.

        Args:
            value (int): value to put into arukone
        """
        # Randomly generate location of
        row = random.randint(0, field_size - 1)
        col = random.randint(0, field_size - 1)
        
        # Check whether spot is empty and that the same number is not directly next to it
        # To detect if the same value is directly neighboring, the first element from each
        # tuple containing (value, row, column) is comprehended into a list. It is then
        # checked whether the list already contains the number
        if field[row][col] == 0 and value not in [element[0] for element in get_surrounding_elements(arr=field, row=row, col=col)]:
            # Fill field
            field[row][col] = value
        else:
            # Regenerate value
            fill_field(value)

    # Iterate over each pair
    for value in range(1, pairs + 1):
        # Fill value twice into arukone
        fill_field(value)
        fill_field(value)

    # Check whether generated arukone is solvable
    if not is_solvable_arukone(field, pairs):
        # Regenerate arukone if it is not solvable
        return generate_arukone(field_size, pairs)

    # Return arukone
    return field


def start_command_line_interface():
    """Starts command line interface that asks user for field size and the number of pairs.
    It then prints a valid arukone.
    """
    # Prompt user for field size and number of pairs
    field_size = int(input("Field size: "))
    pairs = int(input("Number of pairs: "))

    # Neatly print arukone
    for row in generate_arukone(field_size=field_size, pairs=pairs):
        print(' '.join(map(str, row)))


# Check whether generate.py runs as main program
if __name__ == "__main__":
    start_command_line_interface()
