from utility import get_surrounding_elements_2d

import itertools


def find_paths(arukone: list, original_path: list) -> list:
    """Recursively finds all paths that lead from a number to its matching number.

    Args:
        arukone (list): a 2d list of the field. Empty squares have a value of 0
        original_path (list): the path that gets extended

    Returns:
        list: all valid paths
    """
    # Get the location of the last item of the path
    _, row_last_element, col_last_element = original_path[-1]

    # Get the surrounding elements 
    surrounding_elements = get_surrounding_elements_2d(arukone, row_last_element, col_last_element)
    
    paths = []
    valid_paths = []

    # Detect whether path touches itself by checking if there's more than one 
    # common element between the original path and surrounding elements.
    # If it does, the path is discarded. It does not provide a new solution as there is already 
    # a path that branches off earlier and only uses unnecessary computing resources.
    if len(set(original_path).intersection(surrounding_elements)) > 1:
        return []
    
    # Iterate over each surrounding element
    # Each surrounding element provides a part of possible solution and is therefore explored
    for element in surrounding_elements:
        # Get first variable of tuple
        value = element[0]
        
        # Stop lines crossing over themselves
        if element not in original_path:
            if value == original_path[0][0]:
                valid_paths.append(original_path + [element])
                # Stops the path from being extended when it touches endpoint
                return valid_paths
            elif value == 0:
                paths.append(original_path + [element])

    # Continue extending path recursively one element at a time
    for path in paths:
        valid_paths += find_paths(arukone, path)

    # Return the completed list of valid paths for one pair
    return valid_paths


def has_path_combination(all_paths: list) -> bool:
    """Checks if there is a valid combination of paths that connects all pairs of numbers.

    Args:
        all_paths (list): a 3d list containing the paths of all pairs of numbers.

    Returns:
        bool: whether or not there is a valid combination of paths connecting all pairs of numbers
    """
    # Define a function to check if there is no overlap between paths of combination
    def check_no_overlap(combinations):
        # Iterate through each combination of paths
        for combination in combinations:
            # Iterate through all possible, unique combinations of two paths
            for path_a, path_b in itertools.permutations(combination, r=2):
                # Check if there is any intersection (overlap) between the two paths
                if set(path_a).intersection(path_b):
                    # If there is an overlap, break out of the inner loop
                    break
            else:
                # If the for loop never invokes break, there is no overlap
                return True
        # If there is overlap in at least one pair of paths, return False
        return False

    # Generate all possible combinations of paths using itertools.product
    path_combinations = itertools.product(*all_paths)

    # Call the check_no_overlap function with the generated path combinations and return the result
    return check_no_overlap(path_combinations)
