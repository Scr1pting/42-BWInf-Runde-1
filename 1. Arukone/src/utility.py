def get_surrounding_elements_2d(arr: list, row: int, col: int) -> list:
    """Determines the elements that are next to an element in a 2d list.
    Does not determine diagonally adjacent elements.

    Args:
        arr (list): 2d list
        row (int): row of list
        col (int): column of list

    Returns:
        list: contains tuples, each with value, row, column
    """
    # Initialize an empty list to store the surrounding elements
    surrounding = []

    # Determine the number of rows and columns in the 2D list
    num_rows = len(arr)
    num_cols = len(arr[0])

    # Define the relative positions of the surrounding elements
    # Four possible positions: above, left, right, and below the current element
    positions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    # Iterate through each relative position to check for neighboring elements
    for row_offset, col_offset in positions:
        r = row + row_offset  # Calculate the row index of the neighboring element
        c = col + col_offset  # Calculate the column index of the neighboring element

        # Check if the calculated row and column indices are within the bounds of the list
        if 0 <= r < num_rows and 0 <= c < num_cols:
            # If the indices are valid, append a tuple containing
            # value, row index, column index of the neighboring element
            surrounding.append((arr[r][c], r, c))

    return surrounding
