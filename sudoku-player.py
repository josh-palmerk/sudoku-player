

# TODO list:
#       - remove excessive comments; add necessary ones
#       - add autosolve code
#       - add winchecking
#       - add relevant docstrings
#       - should 0 be valid?



import json

def main():
    test_parse()
    test_is_move_valid()
    board = get_board_from_file()
    new_board = play_game(board)
    quit_game(new_board)


# File management

def quit_game(board: list):
    """Exits game, asking if user wishes to save the current board.

    Args:
        board (list): Sudoku board as 2d array
    """
    if input("Would you like to save your board to a file? (y/n) \n> ").lower() == "y":
        filename = prompt_filename()
        save_board_to_file(filename, board)


def get_board_from_file() -> list:
    """Gets sudoku board from a valid user-inputted filename.

    Returns:
        list: sudoku board as 2d array
    """
    valid = False
    data = []
    while not valid:
        filename = prompt_filename()
        
        # Validate filename input
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            valid = True
        except Exception:
            print("Invalid file.")

    return data['board']


def prompt_filename() -> str:
    """Gets a filename from the user.

    Returns:
        str: User-inputted filename
    """
    filename = input("What is the filename? \n> ")
    return filename


def save_board_to_file(filename: str, board: list) -> None:
    """Saves 2d array (board) to local file with specified name.

    Args:
        filename (str)
        board (list): 2d array
    """
    data = {'board': board}
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# Game Management

def play_game(board: list) -> list:

    keep_playing = True
    while keep_playing:
        print_board(board)
        move = prompt_move(board)
        if move["command"] == "quit": # Quit code
            keep_playing = False
        elif move["command"] == "auto_solve": 
            solved = solve_board(board, (0, 0), 1)
            if solved == False:
                print("Failed to autosolve.")
            else:
                print_board(solved[1])
                print("Solved Board Successfully!")
                keep_playing = False
        else:
            board = update_board(move, board)
    
    return board


def prompt_move(board: list) -> dict:

    valid = False
    move = {"command": "play"}
    
    while not valid:

        square = input("Choose a space:\n> ")
        if square == "q":
            move["command"] = "quit" #Quit code
        if square == "auto_solve":
            move["command"] = "auto_solve" #Quit code
            return move
        parsed = parse_input(square)
        
        # Checks if input can be translated to a move. Is_move_valid() verifies legality of move.
        if parsed["parsed_valid"]:
            num = input("What number in that space?\n> ")
            if len(num) == 1 and num.isdigit() and int(num) >= 0: #TODO modularize this?
                move["x"] = parsed["x"]
                move["y"] = parsed["y"]
                move["number"] = int(num)
                response = is_move_valid(move, board)
                valid = response[0]
                print(response[1])
            else:
                print("Invalid number, try again.")
        
        else:
            print("Invalid space, try again.")

    return move


def update_board(move: dict, board: list) -> list:
    """Makes specified move on board, then returns the edited board.

    Args:
        move (list): [(x, y), number]
        board (list): The board to be edited.

    Returns:
        list: The new board.
    """
    board[move["x"]][move["y"]] = move["number"]
    return board


def print_board(board: list) -> None:
    """Prints the board.
    The following code was a collaborative effort between a human programmer and ChatGPT.
    Args:
        board (list): Sudoku board as 2d array
    """
    print("    A B C   D E F   G H I")
    for i in range(9):
        row = board[i]
        # Print row number (1-9) followed by the row contents
        print(f"{i+1}   ", end="") 
        for j in range(9):
            # Print the number with a space, or a blank space if num == 0
            if row[j] == 0:
                print(" ", end=" ")
            else:
                print(row[j], end=" ")
            # Add a "|" after the 3rd and 6th columns
            if j == 2 or j == 5:
                print("|", end=" ")
        # Add a line break after each row, and print separators every 3 rows
        print()
        if i == 2 or i == 5:
            print("   -------+-------+-------")



# Input Validation

def is_move_valid(move: dict, board: list) -> tuple:
    #  Step 1: Parse the input to get row, col, num
    row = move["x"]
    col = move["y"]
    num = move["number"] 
    
    # Step 2: If number is 0, alow user to "clear" the space.
    if num == 0:
        return (False, "Unable to clear spaces in this version.")
 
    #  Step 3: Check if the number is valid in the square the user is trying to edit 
    if not check_square(row, col, board): 
        return (False, "This space is already occupied. Choose an empty space.") 

    #  Step 4: Check if the number is valid in the current row 
    if not check_row(row, num, board): 
        return (False, "The number already exists in this row. Try another number.") 
 
    #  Step 5: Check if the number is valid in the current column 
    if not check_col(col, num, board): 
        return (False, "The number already exists in this column. Try another number.") 

    #  Step 6: Check if the number is valid in the 3x3 sub-box 
    if not check_box(row, col, num, board): 
        return (False, "The number already exists in this 3x3 sub-box. Try another number.") 
 
    #  Step 7: If all checks pass, return success message 
    return (True, "Move is valid. Good job!") 


def check_square(row, col, board): 
    #  Check if the cell is already occupied 
    if board[row][col] != 0: 
        return False  #  The space is occupied by another number 
 
    #  If the cell is empty, return True 
    return True
 
 
def check_row(row, num, board): 
    # Loop through all columns in the given row 
    for col in range(0, 9): 
        #  If the number already exists in the row, return False 
        if board[row][col] == num: 
            return False 
 
    #  If no conflicts, return True 
    return True 
 
 
def check_col(col, num, board): 
    #  Loop through all rows in the given column 
    for row in range(0, 9): 
        #  If the number already exists in the column, return False 
        if board[row][col] == num: 
            return False 
 
    #  If no conflicts, return True 
    return True 


def check_box(row, col, num, board): 
    #  Calculate the top-left corner of the 3x3 sub-box 
    start_row = row - (row % 3)
    start_col = col - (col % 3) 

    #  Loop through the 3x3 sub-box 
    for i in range(start_row , start_row + 3): 
        for j in range(start_col, start_col + 3): 
            #  If the number already exists in this 3x3 box, return False 
            if board[i][j] == num: 
                return False 
 
    #  If no conflicts, return True 
    return True 


def parse_input(input: str) -> dict:
    move = {}
    move["parsed_valid"] = False # default is invalid

    valid_letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'}

    if len(input) != 2:
        return move # invalid
    
    if input[0].isdigit() and input[1].lower() in valid_letters:
        letter = int(ord(input[1].lower())) - int(ord("a"))
        number = int(input[0]) - 1

    elif input[1].isdigit() and input[0].lower() in valid_letters:
        letter = int(ord(input[0].lower())) - int(ord("a"))
        number = int(input[1]) - 1

    else:
        return move # invalid

    move["x"] = number
    move["y"] = letter

    if move["x"] > -1 and move["x"] < 9 and move["y"] > -1 and move["y"] < 9:
        move["parsed_valid"] = True # valid
    return move



# Autosolver

def solve_board(curr_board: list, curr_space, num) -> tuple:
    curr_move = {"x": curr_space[0], "y": curr_space[1], "number": num}
    if not is_move_valid(curr_move, curr_board)[0]:
        return (False, curr_board)
    else: #redundant else
        # Update The Board!! (new_board)
        
        new_board = update_board(curr_move, curr_board)
        next_space = get_next_empty_space(new_board, curr_space[0], curr_space[1])
        if next_space == None:
            return (True, new_board)
    
    # now below code executes only if move was valid but board is not done

    result = solve_board(new_board, next_space, 1)
    if result[0]:
        return result
    result = solve_board(new_board, next_space, 2)
    if result[0]:
        return result    
    result = solve_board(new_board, next_space, 3)
    if result[0]:
        return result    
    result = solve_board(new_board, next_space, 4)
    if result[0]:
        return result    
    result = solve_board(new_board, next_space, 5)
    if result[0]:
        return result    
    result = solve_board(new_board, next_space, 6)
    if result[0]:
        return result    
    result = solve_board(new_board, next_space, 7)
    if result[0]:
        return result
    result = solve_board(new_board, next_space, 8)
    if result[0]:
        return result
    result = solve_board(new_board, next_space, 9)
    if result[0]:
        return result
    #if all fail return false with old board (undo move)
    return (False, curr_board)

def get_next_coordinate(x, y):
    # Check if we're at the last column (8)
    if y < 8:
        return (x, y + 1)  # Move right
    # If we're at the last column, move to the next row
    elif x < 8:
        return (x + 1, 0)  # Move down to the next row, first column
    else:
        return None  # We're at the bottom-right corner (8, 8), no next coordinate


def get_next_empty_space(board, start_x, start_y):
    # Start at the given position and search for the next empty space
    i, j = start_x, start_y
    while True:
        if check_square(board, i, j):  # Check if current space is empty
            return (i, j)  # Return the coordinates of the empty space
        
        # Get the next coordinate to check
        next_coord = get_next_coordinate(i, j)
        
        if next_coord is None:  # If we've reached the end of the grid
            return None  # No empty space found
        
        # Update i, j to the next coordinates
        i, j = next_coord


def test_parse():
    A1 = parse_input("A1")
    assert A1["x"] == 0 and A1["y"] == 0, "end case"

    a1 = parse_input("a1")
    assert a1["x"] == 0 and a1["y"] == 0, "lowercase"
    
    one_a = parse_input("1a")
    assert one_a["x"] == 0 and one_a["y"] == 0, "backwards"
    
    assert A1 == a1 and a1 == one_a, "Equivalence of A1, a1, 1a"
    
    E5 = parse_input("E5")
    assert E5["x"] == 4 and E5["y"] == 4, "Middle Case"
    
    I9 = parse_input("I9")
    assert I9["x"] == 8 and I9["y"] == 8, "End Case"

    B6 = parse_input("B6")
    assert B6["x"] == 5, "x is number and y is letter"
    assert B6["y"] == 1, "x is number and y is letter"

    valid_list = [A1, a1, one_a, E5, I9, B6]
    for item in valid_list:
        assert item["parsed_valid"] == True, "Validity message"

    hello_world = parse_input("hello world")
    assert hello_world["parsed_valid"] == False, "len(input) > 2"
    
    A0 = parse_input("A0")
    assert A0["parsed_valid"] == False, "Invalid square (number)"

    J1 = parse_input("J1")
    assert J1["parsed_valid"] == False, "Invalid square (letter)"
    
    print("All tests passed for parse_input()")


def test_is_move_valid():
    board = []
    with open("hard.json", 'r') as file:
        board = json.load(file)['board']
    
    assert is_move_valid({"x": 0, "y": 0, "number": 1}, board)[0] == False, "Box"
    assert is_move_valid({"x": 0, "y": 0, "number": 5}, board)[0] == False, "Col"
    assert is_move_valid({"x": 0, "y": 0, "number": 2}, board)[0] == True, "Valid"
    assert is_move_valid({"x": 4, "y": 4, "number": 1}, board)[0] == False, "Row and col"
    assert is_move_valid({"x": 4, "y": 4, "number": 8}, board)[0] == True, "Valid"
    assert is_move_valid({"x": 2, "y": 2, "number": 5}, board)[0] == False, "Square filled"
    assert is_move_valid({"x": 0, "y": 8, "number": 8}, board)[0] == False, "Box"
    print("All tests passed for is_move_valid()")


if __name__ == "__main__":
    main()