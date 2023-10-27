import re
import itertools

# python3 -m pip install -U prettytable
from prettytable import PrettyTable

def generate_lights_matrix(construction: list, lamps: dict) -> list:
    lights = [[]]

    for value in construction[0]:
        if value in lamps.keys():
            lights[0].append(lamps[value])
        else:
            # Turn on all remaining lights
            # Replace empty blocks with light-turned-off
           lights[0].append(int(re.sub(r"Q.*", "1", value.replace("X", "0"))))

    for row_index, row in enumerate(construction):
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
                temp_value = 1 if lights[row_index - 1][col_index] + lights[row_index - 1][col_index + 1] == 0 else 0

                lights_in_row.append(temp_value)
                lights_in_row.append(temp_value)

                skip = True
            else:
                lights_in_row.append(lights[row_index - 1][col_index])

        lights.append(lights_in_row)

    return lights

def generate_table(construction: list) -> str:
    lamps = [element for element in construction[0] if element.startswith("Q")]

    lamp_combination_numbers = list(itertools.product([0, 1], repeat=len(lamps)))

    # Create an array of dictionaries with the combinations
    lamp_combinations = [{lamp: value for lamp, value in zip(lamps, combination)} for combination in lamp_combination_numbers]

    sensor_status = []

    for combination in lamp_combinations:
        lights_matrix = generate_lights_matrix(
            construction=construction,
            lamps=combination
        )
        last_row = list(zip(construction[-1], lights_matrix[-1]))

        sensor_status_row = []

        for block_type, status in last_row:
            if block_type.startswith("L"):
                sensor_status_row.append(status)

        sensor_status.append(sensor_status_row)

    combined_status = [list(row1) + row2 for row1, row2 in zip(lamp_combination_numbers, sensor_status)]

    combined_status = [[str(status).replace("0", "Off").replace("1", "On") for status in status_row] for status_row in combined_status]

    table = PrettyTable()

    table.field_names = list(filter(lambda block: block.startswith("Q"), construction[0])) + list(filter(lambda block: block.startswith("L"), construction[-1]))
    table.add_rows(combined_status)

    return table

def start_command_line_interface():
    path_to_construction = input("Path to construction: " )

    while True:
        save_question = input("Save table to disk (yes/no): ")
        if save_question.lower() in ["yes", "y"]:
            print("The table will not be printed to the console.")
            save_path = input("Path to save table: ")
            break
        elif save_question.lower() in ["no", "n"]:
            break
        else:
            print("Invalid input. Please enter yes/no.")

    with open(path_to_construction, "r") as file:
        construction_file = file.readlines()
    
    construction = []

    # Loop through the lines
    for line in construction_file:
        if re.search(r"\d+\s\d+", line) or line.rstrip() == "":
            continue

        # Split the line into individual elements
        elements = line.strip().split()
        
        # Append the elements as a row to the matrix
        construction.append(elements)

    table = generate_table(construction=construction)

    if save_path:
        with open(save_path, "w") as file:
            file.writelines(str(table))
    else:
        print(table)


if __name__ == "__main__":
    start_command_line_interface()
