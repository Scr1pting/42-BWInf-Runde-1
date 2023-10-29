import re
import itertools

# python3 -m pip install -U prettytable
# Used for formatting output
from prettytable import PrettyTable


def generate_lights_matrix(construction: list, lamps: dict) -> list:
    """Generates a 2d list describing whether each field is lit or not.

    Args:
        construction (list): a 2d list following the specification on the BWInf website
        lamps (dict): the state of all initial lamps

    Returns:
        list: a 2d list describing whether each field is lit (1) or not (0)
    """
    # Initialize empty lights matrix
    lights = []

    # Iterate over each row of the construction
    for row_index, row in enumerate(construction):
        lights_in_row = []
        skip = False

        for col_index, value in enumerate(row):
            if skip:
                # Skips the iteration of the loop
                skip = False
                continue

            if value in lamps.keys():
                # Set the value of the initial lamps
                lights_in_row.append(lamps[value])
                print("Set lamps!")
            elif value.startswith("Q"):
                # Default all remaining initial lamps to 0
                lights_in_row.append(1)
            elif row_index == 0:
                # The emptiness in the initial row is not lit as there are no fields preceding it
                lights_in_row.append(0)
            elif value == "r":
                # Fields marked with "r" do not have a sensor but copy the value of fields 
                # marked with a capital "R"
                # When "r" comes first, the capital "R" field comes directly afterwards
                # Fields with capital "R" invert the state of the field that precedes it
                status = 1 - lights[row_index - 1][col_index + 1]

                # Change both the value of lowercase "r" and the value of capital "R"
                lights_in_row.extend([status, status])

                # Both values have already been changed
                # No need to process following "R" field
                skip = True
            elif value == "R":
                # Fields with capital "R" invert the state of the field that precedes it
                status = 1 - lights[row_index - 1][col_index]

                # Change both the value of the capital "R" and of lowercase "r"
                # Lowercase "r" copies the values of capital "R"
                lights_in_row.extend([status, status])

                # Both values have already been changed
                # No need to process following "r" field
                skip = True
            elif value == "W":
                print(row_index)
                # White blocks are off when the two fields that precedes them are both on
                # Otherwise, they are on
                status = 0 if lights[row_index - 1][col_index] + lights[row_index - 1][col_index + 1] == 2 else 1

                # Since white blocks have one uniform state that depend on the sensors of 
                # both fields, both fields are changed
                lights_in_row.extend([status, status])

                # Both values have already been changed
                # No need to process following "W" field
                skip = True
            else:
                # All other fields, like the light sensors, blue fields, and emptiness 
                # copy the state of their preceding blocks
                lights_in_row.append(lights[row_index - 1][col_index])

        # Append completed row of light states
        lights.append(lights_in_row)

    # Return the complete matrix
    return lights


def generate_table(construction: list) -> str:
    """Generates a text table from a construction list. 
    The table details the states of all sensors depending on the state of the initial lamps.

    Args:
        construction (list): a 2d list following the specification on the BWInf website

    Returns:
        str: a text table
    """
    # Get all initial lamps
    lamps = [element for element in construction[0] if element.startswith("Q")]

    # Generate every possible combination of states for all initial lamps
    lamp_combination_numerical = list(itertools.product([0, 1], repeat=len(lamps)))

    # Create a list of dictionaries that each matches lamp with state 
    lamp_combinations = [{lamp: value for lamp, value in zip(lamps, combination)} for combination in lamp_combination_numerical]

    statuses = []

    # Collect the sensor status 
    for combination in lamp_combinations:
        lights_matrix = generate_lights_matrix(construction=construction, lamps=combination)

        # Match the last row of the construction list (descriptions)
        # with the lights matrix (statuses)
        last_row = list(zip(construction[-1], lights_matrix[-1]))

        sensor_statuses = []

        # Only collect sensors as their status is of interest while neglecting empty fields
        for block_type, status in last_row:
            if block_type.startswith("L"):
                sensor_statuses.append(status)

        # Combine lamp combination and sensor statuses
        statuses.append(list(combination.values()) + sensor_statuses)

    # Replace numerical status with descriptive words "On" and "Off"
    statuses = [[str(status).replace("0", "Off").replace("1", "On") for status in status_row] for status_row in statuses]

    table = PrettyTable()

    # Generate table header by extracting initial lamp and sensor labels
    table.field_names = list(filter(lambda field: field.startswith("Q"), construction[0])) + list(filter(lambda field: field.startswith("L"), construction[-1]))
    # Add statuses
    table.add_rows(statuses)

    # Return table
    return table


def start_command_line_interface():
    """
    Starts a command line interface that asks the user for the construction's path,
    whether to save the table, and if so, where to save it.
    
    Either saves or prints the table detailing the states of all sensors depending on 
    the state of the initial lamps.
    """
    path_to_construction = input("Path to construction: " )

    # Continuously ask user whether or not to save the table to the disk until they
    # enter a valid input
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

    # Read construction file
    with open(path_to_construction, "r") as file:
        construction_file = file.readlines()
    
    # Initialize construction list
    # A list is easier to work with than the provided string
    construction = []

    # Loop through the lines
    for line in construction_file:
        # Remove the initial info provided at the beginning of the files and empty lines
        if re.search(r"\d+\s\d+", line) or line.rstrip() == "":
            continue

        # Split the line into individual list elements
        elements = line.strip().split()
        
        # Append the elements as a row to the matrix
        construction.append(elements)

    # Generate table detailing the states of all sensors depending on 
    # the state of the initial lamps
    table = generate_table(construction=construction)

    # Save or print table
    if "save_path" in locals():
        with open(save_path, "w") as file:
            file.writelines(str(table))
    else:
        print(table)


# Check whether main.py runs as main program
if __name__ == "__main__":
    start_command_line_interface()
