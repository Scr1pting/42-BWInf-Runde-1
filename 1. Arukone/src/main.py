from generate import generate_arukone

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

# Check whether main.py runs as main program
if __name__ == "__main__":
    start_command_line_interface()
