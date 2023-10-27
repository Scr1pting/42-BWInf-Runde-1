import re


def generate_lights_matrix(blocks: list) -> list:
    lights = [[int(re.sub(r"Q.*", "1", block.replace("X", "0"))) for block in blocks[0]]]

    for row_index, row in enumerate(blocks):
        if row_index == 0:
            continue

        lights_in_row = []
        skip = False

        for col_index, value in enumerate(row):
            if skip:
                skip = False
                continue

            if value == "X":
                lights_in_row.append(0)
            elif value == "B":
                lights_in_row.append(lights[row_index - 1][col_index])
            elif value == "r":
                temp_value = 1 - lights[row_index - 1][col_index + 1]

                lights_in_row.append(temp_value)
                lights_in_row.append(temp_value)

                skip = True
            elif value == "R":
                temp_value = 1 - lights[row_index - 1][col_index]

                lights_in_row.append(temp_value)
                lights_in_row.append(temp_value)

                skip = True
            elif value == "W":
                temp_value = 1 if lights[row_index][col_index] + lights[row_index - 1][col_index] == 0 else 0

                lights_in_row.append(temp_value)
                lights_in_row.append(temp_value)

                skip = True
            else:
                lights_in_row.append(lights[row_index - 1][col_index])

        lights.append(lights_in_row)

    return lights

# def generate_table(blocks: list) -> str:
    

def start_command_line_interface():
    construction_path = input("Path to construction: " )

    while True:
        save_question = input("Save table to disk (yes/no): ")
        if save_question.lower() in ["yes", "y"]:
            print("The table will not be printed in the console.")
            save_path = input("Path to save table: ")
            break
        elif save_question.lower() in ["no", "n"]:
            break
        else:
            print("Invalid input. Please enter yes/no.")

start_command_line_interface()

print(nandu([
    ['X','X','X','X','X','Q1','Q2','X','X','Q3','Q4','X','X','Q5','Q6','X','X','X','X','X','X','X'],
    ['X','X','X','X','X','R','r','X','X','r','R','X','X','R','r','X','X','X','X','X','X','X'],
    ['X','X','X','X','r','R','R','r','r','R','R','r','r','R','R','r','X','X','X','X','X','X'],  
    ['X','X','X','X','W','W','B','B','W','W','B','B','W','W','B','B','X','X','X','X','X','X'],
    ['X','X','X','r','R','B','B','B','B','B','B','B','B','B','B','R','r','X','X','X','X','X'],
    ['X','X','r','R','B','B','X','B','B','B','B','B','B','B','B','X','R','r','X','X','X','X'],
    ['X','r','R','B','B','R','r','B','B','B','B','B','B','B','B','r','R','R','r','X','X','X'],
    ['X','X','B','B','W','W','B','B','X','B','B','B','B','B','B','W','W','B','B','X','X','X'],  
    ['X','r','R','W','W','W','W','R','r','W','W','W','W','W','W','W','W','W','W','r','X','X'],
    ['X','W','W','B','B','W','W','X','B','B','W','W','B','B','W','W','B','B','R','r','X','X'],
    ['r','R','B','B','B','B','R','r','X','B','B','B','B','B','B','B','B','B','B','R','r','X'],
    ['X','B','B','B','B','B','B','R','r','B','B','B','B','B','B','B','B','B','B','W','W','X'],
    ['r','R','B','B','B','B','B','B','B','B','B','B','B','B','B','B','B','B','B','B','R','r'],
    ['L1','X','X','X','X','L2','X','X','X','X','L3','X','L4','X','X','X','X','X','X','X','L5']
]))

