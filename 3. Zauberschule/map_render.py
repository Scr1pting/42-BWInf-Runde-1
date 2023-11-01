def render_path_tubes(blueprint: list, path: list) -> str:
    guide = blueprint

    for index, element in enumerate(path):
        if index == 0 or index == len(path) - 1 or element == "delay":
            continue

        previous_element = path[index - 1]
        next_element = path[index + 1]
        
        level = element[0]
        row = element[1]
        col = element[2]

        if element[0] != next_element[0]:
            guide[level][row][col] = "!"
        elif element[0] != previous_element[0]:
            guide[level][row][col] = "◯"
        elif element[1] == next_element[1] == previous_element[1]:
            guide[level][row][col] = "─"
        elif element[2] == next_element[2] == previous_element[2]:
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
    guide = blueprint

    for index, element in enumerate(path):
        if index == len(path) - 1 or element == "delay":
            continue
        
        previous_element = path[index - 1]
        next_element = path[index + 1]
        
        level = element[0]
        row = element[1]
        col = element[2]

        if element[0] != next_element[0]:
            guide[level][row][col] = "!"
        elif element[1] < next_element[1]:
            guide[level][row][col] = "v"
        elif element[1] > next_element[1]:
            guide[level][row][col] = "^"
        elif element[2] > next_element[2]:
            guide[level][row][col] = "<"
        elif element[2] < next_element[2]:
            guide[level][row][col] = ">"

    return guide


def render_path(blueprint: list, path: list, render_mode: str) -> list:
    if render_mode == "tubes":
        guide = render_path_tubes(blueprint=blueprint, path=path)
    else:
        guide = render_path_characters(blueprint=blueprint, path=path)

    text_guide = f"{len(blueprint[0])} {len(blueprint[1])}\n"

    for level in guide:
        for row in level:
            for element in row:
                text_guide += element
            text_guide += "\n"
        text_guide += "\n"
    
    text_guide += f"Total length of path: {len(path) - 1}"

    return text_guide
