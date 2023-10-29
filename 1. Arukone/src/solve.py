from utility import get_surrounding_elements


def find_paths(arukone: list, original_path: list) -> list:
    """Recursively finds all paths that lead from a number to its matching number.

    Args:
        arukone (list): a 2d array of the field. Empty squares have a value of 0
        original_path (list): the path that gets extended

    Returns:
        list: all valid paths
    """
    # Get the location of the last item of the path
    _, row_last_element, col_last_element = original_path[-1]

    # Get the surrounding elements 
    surrounding_elements = get_surrounding_elements(arukone, row_last_element, col_last_element)
    
    paths = []
    valid_paths = []

    # Detect whether path touches itself by checking if there's more than one 
    # common element between the original path and surrounding elements.
    # If it does, the path is discarded. It does not provide a new solution as there is already 
    # a path that branches off earlier and only uses unnecessary computing resources.
    if len(set(original_path) & set(surrounding_elements)) > 1:
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


def has_path_combination(all_paths: list, existing_path_combination: list = [], index: int = 0) -> bool:
    """Recursively checks if there is a valid combination of paths that connects
    all pairs of numbers.

    Args:
        all_paths (list): a 3d array containing the paths of all pairs of numbers.
        existing_path_combination (list, optional): A one-dimensional list containing the tuples of the paths of the previously already checked number pairs. Defaults to [].
        index (int, optional): Index of the 3d array. Defaults to 0.

    Returns:
        bool: whether or not there is a valid combination of paths connecting all pairs of numbers
    """

    # TODO Try using itertools to generate all path combinations. Thereby, the maximum recursion depth of 6 can be circumvented

    # Get a list of the paths at the provided index of the all_paths array
    paths = all_paths[index]

    # Iterate of each path 
    for path in paths:
        # Check that there is no overlap between the new path and the existing combination of paths
        if len(set(path) & set(existing_path_combination)) == 0:
            if index == len(all_paths) - 1:
                # Last element in array
                # Means that all previous checks succeeded, and that there is a possible solution
                return True
            else:
                # Not at last check yet
                # Continue checking for the paths that follow.
                value = has_path_combination(
                    all_paths=all_paths,
                    existing_path_combination=existing_path_combination + path,
                    index=index + 1
                )
                
                # Only return a value if that value is True
                # Otherwise, the function would return the value of the first path it examined,
                # even if a valid combination of paths exists
                if value == True:
                    return True

    # Default to False
    return False
