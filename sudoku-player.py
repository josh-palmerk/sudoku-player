
import json

def main():
    #test_parse()
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
        #"D:/dev/sudoku-player/"
        save_board_to_file(filename, board)


def get_board_from_file() -> list:
    """Gets sudoku board from a user-inputted filename.

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
    #TODO change this to play_one_round
    keep_playing = True
    while keep_playing:
        print_board(board)
        move = prompt_move(board)
        if move[1] == -99: # Quit code
            keep_playing = False
        else:
            board = update_board(move, board)
    
    return board


def prompt_move(board: list) -> list:
    """ Returns [(x, y), num] 
    x: column a-i as int 0-8
    y: rows 1-9 as int 0-8
    num: number on board, 1-9
    
    Will return all 3 above ints as -99 if user chooses to quit."""
    valid = False
    move = []
    
    while not valid:
        parse_invalid = (-1, -1)
        square = input("Choose a space:\n> ")
        if square == "q":
            return [(-99, -99), -99] #Quit code
        
        parsed = parse_input(square)
        
        # Checks if input can be translated to a move. Is_move_valid() verifies legality of move.
        if parsed != parse_invalid:
            num = input("What number in that space?\n> ")
            if len(num) == 1 and num.isdigit() and int(num) >= 0: #TODO modularize this
                move = [parsed, int(num)]
                response = is_move_valid(move, board)
                valid = response[0]
                print(response[1])
            else:
                print("Invalid number, try again.")
        
        else:
            print("Invalid space, try again.")

    return move


def update_board(move: list, board: list) -> list:
    """Makes specified move on board, then returns the edited board.

    Args:
        move (list): [(x, y), number]
        board (list): The board to be edited.

    Returns:
        list: The new board.
    """
    space = move[0]
    num = move[1]
    board[space[0]][space[1]] = num
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
            print("     -----+-----+-----")



# Input Validation

def is_move_valid(move, board) -> tuple:
        #  Step 1: Parse the user input to get row, col 
    (row, col) = move[0]
    num = move[1] 
    
    # Step 2: If number is 0, alow user to "clear" the space.
    if num == 0:
        return (True, "Clearing space.")
 
    #  Step 3: Check if the cell is already occupied 
    #if board[row][col] != 0: 
        #return (False, "This space is already occupied. Choose an empty space.") 
 
    #  Step 4: Check if the number is valid in the current row 
    if not check_row(row, num, board): 
        return (False, "The number already exists in this row. Try another number.") 
 
    #  Step 5: Check if the number is valid in the current column 
    if not check_col(col, num, board): 
        return (False, "The number already exists in this column. Try another number.") 

    #  Step 6: Check if the number is valid in the 3x3 sub-box 
    if not check_box(row, col, num, board): 
        return (False, "The number already exists in this 3x3 sub-box. Try another number.") 
 
    #  Step 7: Check if the number is valid in the square the user is trying to edit 
    if not check_square(row, col, board): 
        return (False, "The move is not valid for this square. Try again.") 
 
    #  Step 8: If all checks pass, return success message 
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
    print(start_row)
    start_col = col - (col % 3) 
    print(start_col)

    #  Loop through the 3x3 sub-box 
    for i in range(start_row , start_row + 3): 
        for j in range(start_col, start_col + 3): 
            #  If the number already exists in this 3x3 box, return False 
            if board[i][j] == num: 
                return False 
 
    #  If no conflicts, return True 
    return True 


def parse_input(move: str) -> tuple:
	# Returns -1.-1 if  move is invalid
    invalid = (-1, -1)
    valid_letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'}

    if len(move) != 2:
        return invalid
    
    if move[0].isdigit() and move[1].lower() in valid_letters:
        letter = int(ord(move[1].lower())) - int(ord("a"))
        number = int(move[0]) - 1

    elif move[1].isdigit() and move[0].lower() in valid_letters:
        letter = int(ord(move[0].lower())) - int(ord("a"))
        number = int(move[1]) - 1

    else:
        return invalid

    move = (number, letter)

    if move[0] > -1 and move[0] < 9 and move[1] > -1 and move[1] < 9:
        return move
    else:
        return invalid




#Test functions

def test_is_move_valid():
    board = []
    with open("hard.json", 'r') as file:
        board = json.load(file)['board']
    
    assert is_move_valid(((0, 0), 1), board)[0] == False, "Box"
    assert is_move_valid(((0, 0), 5), board)[0] == False, "Col"
    assert is_move_valid(((0, 0), 2), board)[0] == True,  "Valid"
    assert is_move_valid(((4, 4), 1), board)[0] == False, "Row and col"
    assert is_move_valid(((4, 4), 8), board)[0] == True,  "Valid"
    assert is_move_valid(((2, 2), 5), board)[0] == False, "Square filled"
    assert is_move_valid(((0, 8), 8), board)[0] == False, "Box"
    print("All cases passed for is_move_valid()")


def test_parse():
    print("\nparse A1")
    print(parse_input("A1"))
    print("\nparse B2")
    print(parse_input("B2"))
    print("\nparse hello")
    print(parse_input("hello"))
    print("\nparse C2")
    print(parse_input("C2"))
    print("\nparse D5")
    print(parse_input("D5"))
    print("\nparse I9")
    print(parse_input("I9"))
    print("\nparse J0")
    print(parse_input("J0"))
    print("\nparse 11")
    print(parse_input("11"))
    print("\nparse BB")
    print(parse_input("BB"))
    print("\nparse 1A")
    print(parse_input("1A"))
    print("\nparse 2C")
    print(parse_input("2C"))
    print("\nparse 1a")
    print(parse_input("1a"))


if __name__ == "__main__":
    main()