def sequential_line(filepath: str, _counter=[0]):
    # Define a counter variable to keep track of the current line
    counter = _counter[0]

    with open(filepath, 'r') as file:
        keys = file.readlines()

    if not keys or counter >= len(keys):
        return False

    # Select the current line based on the counter
    selected_line = keys[counter]

    # Increment the counter for the next call
    counter += 1

    if counter >= len(keys):
        # If counter exceeds the number of lines in the file, return False
        return False

    _counter[0] = counter  # Update the counter in the mutable list

    return selected_line.strip()
