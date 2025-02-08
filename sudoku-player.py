import json

def main():
    #test()
    
    board = get_board_from_file()
    new_board = play_game(board)
    quit_game(new_board)


# File management

def quit_game(board: list):
    if input("Would you like to save your board to a file? (y/n) \n> ").lower() == "y":
        filename = prompt_filename()
        #"D:/dev/sudoku-player/"
        save_board_to_file(filename, board)

def get_board_from_file() -> list:
    valid = False
    data = []
    while not valid:
        filename = prompt_filename()
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            valid = True
        except Exception: # as e:
            print("Invalid file.")
            # print(e)
    return data['board']


def prompt_filename() -> str:
    filename = input("What is the filename? \n> ")
    return filename


def save_board_to_file(filename: str, board) -> None:
    data = {'board': board}
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# Game Management

def play_game(board: list) -> list:
    """Handles main game loop."""
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
            if len(num) == 1 and num.isdigit() and int(num) > 0: #TODO modularize this
                move = [parsed, int(num)]
                valid = is_move_valid(move, board)
            else:
                print("Invalid number, try again.")
        
        else:
            print("Invalid space, try again.")

    return move


def update_board(move: list, board: list) -> list:
    space = move[0]
    num = move[1]
    board[space[1]][space[0]] = num
    return board


def print_board(board: list) -> None:
    """Prints the board.
    The following code was a collaborative effort between a human programmer and ChatGPT."""
    print("  A B C   D E F   G H I")
    for i in range(9):
        row = board[i]
        # Print row number (1-9) followed by the row contents
        print(f"{i+1} ", end="") 
        for j in range(9):
            # Print the number with a space
            print(row[j], end=" ")
            # Add a "|" after the 3rd and 6th columns
            if j == 2 or j == 5:
                print("|", end=" ")
        # Add a line break after each row, and print separators every 3 rows
        print()
        if i == 2 or i == 5:
            print("   -----+-----+-----")



# Input Validation

def is_move_valid(move, board):
    return True # TODO

def parse_input(move: str) -> tuple:
	# Returns -1.-1 if  move is invalid
    invalid = (-1, -1)

    if len(move) != 2:
        return invalid
    try: #TODO replace try with typecheck
        x = int(ord(move[0].lower())) - int(ord("a"))
        y = int(move[1]) - 1
        move = (x, y)
    except Exception as e:
        print(e)
        return invalid

    if move[0] > -1 and move[0] < 9 and move[1] > -1 and move[1] < 9:
        return move
    else:
        return invalid



#Test functions

def test():
    print("\nparse A1")
    print(parse_input("A1"))
    print("\nparse B2")
    print(parse_input("B2"))
    print("\nparse hello")
    print(parse_input("hello"))
    print("\nparse C3")
    print(parse_input("C3"))
    print("\nparse D4")
    print(parse_input("D4"))
    print("\nparse I9")
    print(parse_input("I9"))
    print("\nparse J0")
    print(parse_input("J0"))
    print("\nparse 11")
    print(parse_input("11"))
    print("\nparse BB")
    print(parse_input("BB"))


if __name__ == "__main__":
    main()