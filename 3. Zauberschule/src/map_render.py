def render_path_lines(blueprint: list, path: list) -> list:
    """Renders path as text lines. May break when using a non-monospace font.

    Args:
        blueprint (list): 3d list of each fields string value
        path (list): tuples, each containing a field's location (level, row, column)
            or "delay" when it serves to compensate for moving level's,
            which takes 3 times as long as moving in one level 

    Returns:
        list: the guide
    """
    guide = blueprint

    # Iterate over the blueprint
    for index, element in enumerate(path):
        # Skip the first and last element as well as delays
        if index == 0 or index == len(path) - 1 or element == "delay":
            continue

        previous_element = path[index - 1]
        next_element = path[index + 1]
        
        level = element[0]
        row = element[1]
        col = element[2]

        if element[0] != next_element[0]:  # Level change outgoing (different level)
            guide[level][row][col] = "!"
        elif element[0] != previous_element[0]:  # Level change receiving (different level)
            guide[level][row][col] = "◯"
        elif element[1] == next_element[1] == previous_element[1]:  # Same row
            guide[level][row][col] = "─"
        elif element[2] == next_element[2] == previous_element[2]:  # Same column
            guide[level][row][col] = "│"
        elif (element[1] > next_element[1] and element[2] < previous_element[2]
              or element[1] > previous_element[1] and element[2] < next_element[2]):
            guide[level][row][col] = "└"
        elif (element[1] > next_element[1] and element[2] > previous_element[2]
              or element[1] > previous_element[1] and element[2] > next_element[2]):
            guide[level][row][col] = "┘"
        elif (element[1] < next_element[1] and element[2] < previous_element[2]
              or element[1] < previous_element[1] and element[2] < next_element[2]):
            guide[level][row][col] = "┌"
        elif (element[1] < next_element[1] and element[2] > previous_element[2]
              or element[1] < previous_element[1] and element[2] > next_element[2]):
            guide[level][row][col] = "┐"
    
    return guide
        

def render_path_characters(blueprint: list, path: list) -> str:
    """Renders path as character signifying the direction of movement.

    Args:
        blueprint (list): 3d list of each fields string value
        path (list): tuples, each containing a field's location (level, row, column)
            or "delay" when it serves to compensate for moving level's,
            which takes 3 times as long as moving in one level 

    Returns:
        list: the guide
    """
    guide = blueprint

    for index, element in enumerate(path):
        # Skip the first and last element as well as delays
        if index == len(path) - 1 or element == "delay":
            continue
        
        next_element = path[index + 1]
        
        level = element[0]
        row = element[1]
        col = element[2]

        if element[0] != next_element[0]:  # Level change
            guide[level][row][col] = "!"
        elif element[1] < next_element[1]:  # Move up
            guide[level][row][col] = "v"
        elif element[1] > next_element[1]:  # Move down
            guide[level][row][col] = "^"
        elif element[2] > next_element[2]:  # Move left
            guide[level][row][col] = "<"
        elif element[2] < next_element[2]:  # Move right
            guide[level][row][col] = ">"

    return guide


def render_path(blueprint: list, path: list, render_mode="characters") -> str:
    """Creates a text guide of a path, either by using characters or lines.

    Args:
        blueprint (list): 3d list of each fields string value
        path (list): tuples, each containing a field's location (level, row, column)
            or "delay" when it serves to compensate for moving level's,
            which takes 3 times as long as moving in one level 
        render_mode (str): either "characters" or "lines". Defaults to characters

    Returns:
        str: text guide
    """
    # Create guide list
    if render_mode == "lines":
        guide_list = render_path_lines(blueprint=blueprint, path=path)
    else:
        guide_list = render_path_characters(blueprint=blueprint, path=path)

    # Start text guide with the blueprint's dimensions
    text_guide = f"{len(blueprint[0])} {len(blueprint[1])}\n"

    # Iterate over each element of the blueprint and append it without spaces
    for level in guide_list:
        for row in level:
            for element in row:
                text_guide += element
            text_guide += "\n"
        text_guide += "\n"
    
    # Finish guide by stating its length
    text_guide += f"Total length of path: {len(path) - 1} seconds"

    return text_guide
