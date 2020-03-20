"""Visualization module.

This module contains the code needed to visualize the application correctly.

The module includes:

    - Necessary functions to develop game's visualization.
    - Game's graphic interfaces, which include headers, modes' different menus 
      and options, board visualizations...

Visualization module is the second part of 'Chess Masters's application and 
includes all the visuals in game.

Visualization module does not need the importation of the previous Rules 
module but they're not independent at all. The pieces' classes and other 
functionalities are used here. So they do need to work together to the correct 
functioning of the application.

"""



##### IMPORTS #####

# The first one only used for Jupyter files ('.ipynb' extension).
from IPython.display import clear_output
from os import system, name



##### CONSTANTS #####

"""
The constant 'COLS' represents the name of the columns in board, while 'ROWS' 
represents rows' name.

The 'BOARD_ROWS' and 'BOARD_COLS' constants represent, respectively, a pair 
of dictionaries that map position coordinates with their correspondant row 
and col in the board matrix.

The 'PIECES_SYMBOL' constant is a dictionary that traduces a piece's name and 
color to its correspondant symbol.

"""

ROWS = "12345678"
COLS = "abcdefgh"

BOARD_ROWS = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
BOARD_COLS = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
PIECES_SYMBOL = {"Rw": "♖", "Nw": "♘", "Bw": "♗", "Qw": "♕", "Kw": "♔", "Pw": "♙", 
                 "Rb": "♜", "Nb": "♞", "Bb": "♝", "Qb": "♛", "Kb": "♚", "Pb": "♟"}



##### FUNCTIONS #####

def screen_reset():
    """Clear the output to reset the screen."""
    # Clear output in Jupyter files ('.ipynb' extension).
    clear_output(wait=True)                  

    # Clear output in Python files ('.py' extension).
    #system("cls") if name == "nt" else system("clear")


def get_square_col(position):
    """Return the index of a column in the board matrix from a position."""
    return BOARD_COLS[position[0]]


def get_square_row(position):
    """Return the index of a row in the board matrix from a position."""
    return BOARD_ROWS[position[1]]


def get_piece_symbol(piece):
    """Return the symbol of a chess piece from a piece instance."""
    return PIECES_SYMBOL[piece.name + piece.color]


def empty_chessboard():
    """Create an empty board matrix."""

    chessboard = [[" ", " ", " ", " ", " ", " ", " ", " "],
                  [" ", " ", " ", " ", " ", " ", " ", " "],
                  [" ", " ", " ", " ", " ", " ", " ", " "],
                  [" ", " ", " ", " ", " ", " ", " ", " "],
                  [" ", " ", " ", " ", " ", " ", " ", " "],
                  [" ", " ", " ", " ", " ", " ", " ", " "],
                  [" ", " ", " ", " ", " ", " ", " ", " "],
                  [" ", " ", " ", " ", " ", " ", " ", " "]]
    
    return chessboard


def introduce(piece, chessboard):
    """Introduce a piece in the board matrix."""
    col = get_square_col(piece.position)
    row = get_square_row(piece.position)
    piece_symbol = get_piece_symbol(piece)
    chessboard[row][col] = piece_symbol


def print_chessboard(chessboard):
    """Print the board matrix."""
    for line in chessboard:
        print(" ".join(line))
        
        
def set_chessboard(pieces):
    """Set the pieces in the board matrix."""
    chessboard = empty_chessboard()
    for piece in pieces:
        introduce(piece, chessboard)  
    return chessboard


def format_notation(notation):
    """Format the complete game notation."""
    f_notation = []
    if len(notation[0]) > len(notation[1]):
        notation[1].append("...")
    for w_moves, b_moves in zip(notation[0], notation[1]):
        f_notation.append([w_moves, b_moves])
    if "..." in notation[1]:
        notation[1].remove("...")
    return f_notation


def get_print_notation(chess_move, color):
    """Return the print format notation of a given chess move."""
    if chess_move[0] in "PRNBQK":
        symbol = PIECES_SYMBOL[chess_move[0] + color]
        return f"{symbol} {chess_move[1:6]} {chess_move[6:]}".ljust(12)
    elif "0-0" in chess_move:
        return f"  {chess_move}".ljust(12)
    else:
        return chess_move.center(12)


def set_chess_notation(notation):
    """Return the print format notation from the complete game."""
    chess_notation = []
    for i, i_move in enumerate(notation):
        if i == 0:
            chess_notation.append("   " + "White".center(12) + "  ·  " + "Black".center(12))
            continue
        w_move = get_print_notation(i_move[0], "w") if i_move[0] else " "
        b_move = get_print_notation(i_move[1], "b") if i_move[1] else " "
        number = " " + str(i) if i < 10 else str(i)
        chess_notation.append(number + ". " + "  ·  ".join([w_move, b_move]) + ";")
    return chess_notation


def get_result_notation(result):
    """Return the print format notation of the game result."""
    return f"{result[0]}  -  {result[1]}".center(38)


def is_index(number):
    """Return 'True' if a number is a positive index. Otherwise returns 'False'."""
    return True if number > 0 else False


def get_print_setting_notation(piece_input):
    """Return the print format notation of the introduced piece in setting mode."""
    symbol = PIECES_SYMBOL[piece_input[0] + piece_input[1]]
    position = piece_input[3:]
    return f"{symbol} {position}".center(12)


def set_chess_setting_notation(setting_notation):
    """Return the print format notation from setting mode."""
    chess_notation = []
    
    while len(setting_notation[0]) != len(setting_notation[1]):
        if len(setting_notation[0]) > len(setting_notation[1]):
            setting_notation[1].append("...".center(12))
        else:
            setting_notation[0].append("...".center(12))
     
    i = 0
    for w_piece, b_piece in zip(setting_notation[0], setting_notation[1]):
        if not i:
            chess_notation.append("   " + "White".center(12) + "  ·  " + "Black".center(12))
            i += 1
            continue
        number = " " + str(i) if i < 10 else str(i)
        chess_notation.append(number + ". " + "  ·  ".join([w_piece, b_piece]) + ";")
        i += 1
    return chess_notation


##### GAME INTERFACES #####


def print_main_interface():
    """Print the interface in the game main menu."""

    print("""
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
*                                                                                                            *
*                                                                                                            *
*    ██████╗██╗  ██╗███████╗███████╗███████╗   ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ ███████╗  *
*   ██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝   ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝  *
*   ██║     ███████║█████╗  ███████╗███████╗   ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝███████╗  *
*   ██║     ██╔══██║██╔══╝  ╚════██║╚════██║   ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗╚════██║  *
*   ╚██████╗██║  ██║███████╗███████║███████║   ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║███████║  *
*    ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝  *
*                                                                                                            *
*                                                                                                            *
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
==============================================================================================================                                                                                                        

[❶ PLAY A GAME] [❷ SET AND PLAY] [❸ ANALYZE A GAME] [❹ SOLVE A PROBLEM] [❺ ABOUT THE GAME] [❻ EXIT THE GAME]

==============================================================================================================



                                           -----------------
                                       8. | ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ |
                                       7. | ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ | 
                                       6. |                 |
                                       5. |                 |
                                       4. |                 |
                                       3. |                 |
                                       2. | ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ |
                                       1. | ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ |
                                           -----------------
                                            a b c d e f g h



==============================================================================================================
    """)


def print_play_game_header():
    """Print the header in the 'Play a game' mode interface."""

    print("""
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
*                                                                                                            *
*                                                                                                            *
*            ██████  ██       █████  ██    ██      █████       ██████   █████  ███    ███ ███████            *
*            ██   ██ ██      ██   ██  ██  ██      ██   ██     ██       ██   ██ ████  ████ ██                 *
*            ██████  ██      ███████   ████       ███████     ██   ███ ███████ ██ ████ ██ █████              *
*            ██      ██      ██   ██    ██        ██   ██     ██    ██ ██   ██ ██  ██  ██ ██                 *
*            ██      ███████ ██   ██    ██        ██   ██      ██████  ██   ██ ██      ██ ███████            *
*                                                                                                            *
*                                                                                                            *
*                                                                                                            *
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
    """)


def print_play_game_menu():
    """Print the menu in the 'Play a game' mode interface."""

    print("""
    

                                 ■ ═══════════════════════════════════════ ■
                                 ║                                         ║
                                 ║      1. Information about the mode      ║ 
                                 ║                                         ║
                                 ║      2. Play a Classic game             ║
                                 ║                                         ║
                                 ║      3. Play a Fischer game             ║
                                 ║                                         ║
                                 ║      4. Return to main menu             ║
                                 ║                                         ║
                                 ■ ═══════════════════════════════════════ ■
                                 


==============================================================================================================
    """)



def print_play_game_playing(pieces, notation, result=None):
    """Print the in game interface in the playing mode."""
    chessboard = set_chessboard(pieces)
    chess_notation = set_chess_notation(format_notation(notation))
    number = len(chess_notation)

    print(f"""


                      ★ CHESSBOARD ★                              ★ NOTATION ★

                    -----------------                  {chess_notation[0]}
                8. | {" ".join(chessboard[0])} |                                                 
                7. | {" ".join(chessboard[1])} |                {chess_notation[number-4] if is_index(number-4) else ""}
                6. | {" ".join(chessboard[2])} |                {chess_notation[number-3] if is_index(number-3) else ""}
                5. | {" ".join(chessboard[3])} |                {chess_notation[number-2] if is_index(number-2) else ""}
                4. | {" ".join(chessboard[4])} |                {chess_notation[number-1] if is_index(number-1) else ""}
                3. | {" ".join(chessboard[5])} |                                                
                2. | {" ".join(chessboard[6])} |                {get_result_notation(result) if result else ""}                        
                1. | {" ".join(chessboard[7])} |                                                                 
                    -----------------
                     a b c d e f g h
            
            
              
=============================================================================================================            
            
                          ✪  Introduce 'OPTIONS' to get to the options menu  ✪

                   ✪  Move input format example: Ng1-f3 moves Knight from ♞g1 to f3  ✪ 
                      
============================================================================================================= 
    """)


def print_play_game_options(pieces):
    """Print the options interface in the playing mode."""
    chessboard = set_chessboard(pieces)

    print(f"""

                      ★ CHESSBOARD ★                              ★ OPTIONS ★

                    -----------------                  
                8. | {" ".join(chessboard[0])} |                   ┌─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐                         
                7. | {" ".join(chessboard[1])} |                   │                             │
                6. | {" ".join(chessboard[2])} |                   │    1. Help                  │ 
                5. | {" ".join(chessboard[3])} |                   │    2. Save game             │
                4. | {" ".join(chessboard[4])} |                   │    3. Back to game          │
                3. | {" ".join(chessboard[5])} |                   │    4. Return to main menu   │                                         
                2. | {" ".join(chessboard[6])} |                   │                             │                              
                1. | {" ".join(chessboard[7])} |                   └─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘                                                         
                    -----------------
                     a b c d e f g h
            
            

=============================================================================================================   
    """)
    

def print_play_game_help():
    """Print the help command in the playing mode."""

    print("""
    ⇨ Playing move input format:
    
    To introduce a move in the playing mode, follow the default syntax:
    
    The syntax includes the name of the piece which is going to be moved followed by
    the original and final position separated by a hyphen ('-').
    
    - The name of the piece is represented by its name's first capital letter in English.
    - Original and final positions are represented by their coordinates, columns from 'a'
      to 'h' and rows from '1' to '8'.

    · Remember:

        ♖ R Rook ♜ - ♘ N Knight ♞ - ♗ B Bishop ♝ - ♕ Q Queen ♛ - ♔ K King ♚ - ♙ P Pawn ♟ 
    
    The special castling move follows the syntax '0-0' for kingside castling and '0-0-0'
    for queenside castling.
    
    Examples:
                - To move a Knight from 'g1' to 'f3' the syntax is: 'Ng1-f3'
                - To move a King from 'a1' to 'b2' the syntax is: 'Ka1-b2'
                - To move a Pawn from 'd7' to 'd8' the syntax is: 'Pd7-d8'
                - To make the special move kingside castling the syntax is: '0-0'
    
    
==============================================================================================================
    """)


def print_set_and_play_header():
    """Print the header in the 'Set and play' mode interface."""

    print("""
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
*                                                                                                            *
*                                                                                                            *
*        ███████ ███████ ████████      █████  ███    ██ ██████      ██████  ██       █████  ██    ██         * 
*        ██      ██         ██        ██   ██ ████   ██ ██   ██     ██   ██ ██      ██   ██  ██  ██          *
*        ███████ █████      ██        ███████ ██ ██  ██ ██   ██     ██████  ██      ███████   ████           *
*             ██ ██         ██        ██   ██ ██  ██ ██ ██   ██     ██      ██      ██   ██    ██            *
*        ███████ ███████    ██        ██   ██ ██   ████ ██████      ██      ███████ ██   ██    ██            *                                                                                 *                                                                                                            *
*                                                                                                            *
*                                                                                                            *
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
    """)


def print_set_and_play_menu():
    """Print the menu in the 'Set and play' mode interface."""

    print("""
    
    

                                 ■ ═══════════════════════════════════════ ■
                                 ║                                         ║
                                 ║                                         ║ 
                                 ║      1. Information about the mode      ║
                                 ║                                         ║
                                 ║      2. Set and play a game             ║
                                 ║                                         ║
                                 ║      3. Return to main menu             ║
                                 ║                                         ║
                                 ║                                         ║
                                 ■ ═══════════════════════════════════════ ■
                                 



==============================================================================================================
    """)


def print_set_and_play_setting(pieces, setting_notation):
    """Print the interface in the setting mode."""
    chessboard = set_chessboard(pieces)
    chess_notation = set_chess_setting_notation(setting_notation)
    number = len(chess_notation)

    print(f"""


                      ★ CHESSBOARD ★                              ★ NOTATION ★

                    -----------------                  {chess_notation[0]}
                8. | {" ".join(chessboard[0])} |                                                 
                7. | {" ".join(chessboard[1])} |                {chess_notation[number-6] if is_index(number-6) else ""}
                6. | {" ".join(chessboard[2])} |                {chess_notation[number-5] if is_index(number-5) else ""}
                5. | {" ".join(chessboard[3])} |                {chess_notation[number-4] if is_index(number-4) else ""}
                4. | {" ".join(chessboard[4])} |                {chess_notation[number-3] if is_index(number-3) else ""}
                3. | {" ".join(chessboard[5])} |                {chess_notation[number-2] if is_index(number-2) else ""}                                
                2. | {" ".join(chessboard[6])} |                {chess_notation[number-1] if is_index(number-1) else ""}                      
                1. | {" ".join(chessboard[7])} |                                                                 
                    -----------------
                     a b c d e f g h
            
            
              
=============================================================================================================            
            
                          ✪  Introduce 'OPTIONS' to get to the options menu  ✪

                   ✪  Set piece input format example: Rw-e4 sets a white rook in '♖e4'  ✪ 
                      
============================================================================================================= 
    """)
    
    
def print_set_and_play_options(pieces):
    """Prints the options interface in the setting mode."""
    chessboard = set_chessboard(pieces)

    print(f"""

                      ★ CHESSBOARD ★                              ★ OPTIONS ★

                    -----------------                  
                8. | {" ".join(chessboard[0])} |                   ┌─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐                         
                7. | {" ".join(chessboard[1])} |                   │                             │
                6. | {" ".join(chessboard[2])} |                   │    1. Help                  │ 
                5. | {" ".join(chessboard[3])} |                   │    2. Back to game          │
                4. | {" ".join(chessboard[4])} |                   │    3. Return to main menu   │
                3. | {" ".join(chessboard[5])} |                   │                             │                                         
                2. | {" ".join(chessboard[6])} |                   └─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘                              
                1. | {" ".join(chessboard[7])} |                                                                           
                    -----------------
                     a b c d e f g h
            
            

=============================================================================================================   
    """)
    
    
def print_set_and_play_help():
    """Print the help command in the setting mode."""

    print("""
    ⇨ Setting piece input format:
    
    To introduce a piece in the board in setting mode, follow the default syntax:
    
    The syntax includes the name and color of the piece which is going to be set, followed 
    by the position it is going to occup in the board.
    
    - The name of the piece is represented by its name's first capital letter in English.
    - The color of the piece is represented by 'w' when it is white and 'b' otherwise.
    - The position is represented by its coordinates, columns from 'a' to 'h' and rows from
      '1' to '8'.

    · Remember:

        ♖ R Rook ♜ - ♘ N Knight ♞ - ♗ B Bishop ♝ - ♕ Q Queen ♛ - ♔ K King ♚ - ♙ P Pawn ♟ 
    
    Examples:
                - To set a white Rook in 'e4' the syntax is: 'Rw-e4'
                - To set a black Queen in 'g5' the syntax is: 'Qb-g5'
                - To set a black Bishop in 'b7' the syntax is: 'Bb-b7'
    
    
==============================================================================================================
    """)


def print_analyze_game_header():
    """Print the header in the 'Analyze a game' mode interface."""

    print("""
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
*                                                                                                            *
*                                                                                                            *
*   █████  ███    ██  █████  ██   ██    ██ ███████ ███████    █████      ██████   █████  ███    ███ ███████  *
*  ██   ██ ████   ██ ██   ██ ██    ██  ██     ███  ██        ██   ██    ██       ██   ██ ████  ████ ██       *
*  ███████ ██ ██  ██ ███████ ██     ████     ███   █████     ███████    ██   ███ ███████ ██ ████ ██ █████    *
*  ██   ██ ██  ██ ██ ██   ██ ██      ██     ███    ██        ██   ██    ██    ██ ██   ██ ██  ██  ██ ██       *
*  ██   ██ ██   ████ ██   ██ ███████ ██    ███████ ███████   ██   ██     ██████  ██   ██ ██      ██ ███████  *                                                          *                      *                                                                                                            *
*                                                                                                            *
*                                                                                                            *
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
    """)


def print_analyze_game_menu():
    """Print the menu in the 'Analyze a game' mode interface."""

    print("""
    

    
                                 ■ ═══════════════════════════════════════ ■
                                 ║                                         ║
                                 ║                                         ║ 
                                 ║      1. Information about the mode      ║
                                 ║                                         ║
                                 ║      2. Analyze a game                  ║
                                 ║                                         ║
                                 ║      3. Return to main menu             ║
                                 ║                                         ║
                                 ║                                         ║
                                 ■ ═══════════════════════════════════════ ■
                                 



==============================================================================================================
    """)
    

def print_analyze_game_playing(pieces, notation, players, tournament, result=None):
    """Print the in game interface in the analyzing mode."""
    chessboard = set_chessboard(pieces)
    chess_notation = set_chess_notation(format_notation(notation))
    number = len(chess_notation)

    print(f"""


                      ★ CHESSBOARD ★                              ★ NOTATION ★

                    -----------------                  {players[0].center(16) + " · " + players[1].center(16)}
                8. | {" ".join(chessboard[0])} |                {tournament.center(36)}                                 
                7. | {" ".join(chessboard[1])} |                
                6. | {" ".join(chessboard[2])} |                {chess_notation[number-4] if is_index(number-4) else ""}
                5. | {" ".join(chessboard[3])} |                {chess_notation[number-3] if is_index(number-3) else ""}
                4. | {" ".join(chessboard[4])} |                {chess_notation[number-2] if is_index(number-2) else ""}
                3. | {" ".join(chessboard[5])} |                {chess_notation[number-1] if is_index(number-1) else ""}                                
                2. | {" ".join(chessboard[6])} |                                       
                1. | {" ".join(chessboard[7])} |                {get_result_notation(result) if result else ""}                                                  
                    -----------------
                     a b c d e f g h
            
            
              
=============================================================================================================            
            
                          ✪  Introduce 'OPTIONS' to get to the options menu  ✪

             ✪  Available commands: 'N' to take a move forward - 'B' to take a move back  ✪ 
                      
============================================================================================================= 
    """)
    
    
def print_analyze_game_options(pieces):
    """Print the options interface in the analyzing mode."""
    chessboard = set_chessboard(pieces)

    print(f"""

                      ★ CHESSBOARD ★                              ★ OPTIONS ★

                    -----------------                  
                8. | {" ".join(chessboard[0])} |                   ┌─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐                         
                7. | {" ".join(chessboard[1])} |                   │                             │
                6. | {" ".join(chessboard[2])} |                   │    1. Help                  │ 
                5. | {" ".join(chessboard[3])} |                   │    2. Back to game          │
                4. | {" ".join(chessboard[4])} |                   │    3. Return to main menu   │
                3. | {" ".join(chessboard[5])} |                   │                             │                                         
                2. | {" ".join(chessboard[6])} |                   └─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘                              
                1. | {" ".join(chessboard[7])} |                                                                           
                    -----------------
                     a b c d e f g h
            
            

=============================================================================================================   
    """)   
    

def print_analyze_game_help():
    """Print the help command in the analyzing mode."""

    print("""
    ⇨ Analyzing command input format:
    
    In this mode there only exist two commands available:
    
    - The 'Next' command to take a move forward in the game (→).
    - The 'Back' command to take a move back in the game (←).
    
    To introduce a command while analyzing, follow the default syntax:
    
    Examples:
                - To take a move forward the syntax is: 'NEXT' or 'N'
                - To take a move back the syntax is: 'BACK' or 'B'
    
    
==============================================================================================================
    """)


def print_solve_problem_header():
    """Print the header in the 'Solve a problem' mode interface."""

    print("""
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
*                                                                                                            *
*                                                                                                            *
* ███████  █████  ██    ██    ██ ██████    █████    ██████  ██████   █████  ██████  ██     ██████ ███    ███ *
* ██      ██   ██ ██    ██    ██ ██       ██   ██   ██   ██ ██   ██ ██   ██ ██   ██ ██     ██     ████  ████ *
* ███████ ██   ██ ██    ██    ██ █████    ███████   ██████  ██████  ██   ██ ██████  ██     █████  ██ ████ ██ *
*      ██ ██   ██ ██     ██  ██  ██       ██   ██   ██      ██   ██ ██   ██ ██   ██ ██     ██     ██  ██  ██ *
* ███████  █████  ██████  ████   ██████   ██   ██   ██      ██   ██  █████  ██████  ██████ ██████ ██      ██ *                                                         *                       *                                                                                                            *
*                                                                                                            *
*                                                                                                            *
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
    """)
    

def print_solve_problem_menu():
    """Print the menu in the 'Solve a problem' mode interface."""
    
    print("""
    
    

                                 ■ ═══════════════════════════════════════ ■
                                 ║                                         ║
                                 ║                                         ║ 
                                 ║      1. Information about the mode      ║
                                 ║                                         ║
                                 ║      2. Solve a problem                 ║
                                 ║                                         ║
                                 ║      3. Return to main menu             ║
                                 ║                                         ║
                                 ║                                         ║
                                 ■ ═══════════════════════════════════════ ■
                                 



==============================================================================================================
    """)


def print_solve_problem_playing(pieces, notation, players, tournament, result=None):
    """Print the in game interface in the solving mode."""
    chessboard = set_chessboard(pieces)
    chess_notation = set_chess_notation(format_notation(notation))
    number = len(chess_notation)

    print(f"""


                      ★ CHESSBOARD ★                              ★ NOTATION ★

                    -----------------                  {players[0].center(16) + " · " + players[1].center(16)}
                8. | {" ".join(chessboard[0])} |                {tournament.center(36)}                                 
                7. | {" ".join(chessboard[1])} |                
                6. | {" ".join(chessboard[2])} |                {chess_notation[number-4] if is_index(number-4) else ""}
                5. | {" ".join(chessboard[3])} |                {chess_notation[number-3] if is_index(number-3) else ""}
                4. | {" ".join(chessboard[4])} |                {chess_notation[number-2] if is_index(number-2) else ""}
                3. | {" ".join(chessboard[5])} |                {chess_notation[number-1] if is_index(number-1) else ""}                                
                2. | {" ".join(chessboard[6])} |                                       
                1. | {" ".join(chessboard[7])} |                {get_result_notation(result) if result else ""}                                                  
                    -----------------
                     a b c d e f g h
            
            
              
=============================================================================================================            
            
                          ✪  Introduce 'OPTIONS' to get to the options menu  ✪

                   ✪  Move input format example: Ng1-f3 moves Knight from ♞g1 to f3  ✪ 

                  ✪  Available commands: 'H' to get a hint - 'S' to get the solution  ✪ 
                      
============================================================================================================= 
    """)

    
def print_solve_problem_options(pieces):
    """Print the options interface in the solving mode."""
    chessboard = set_chessboard(pieces)

    print(f"""

                      ★ CHESSBOARD ★                              ★ OPTIONS ★

                    -----------------                  
                8. | {" ".join(chessboard[0])} |                   ┌─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐                         
                7. | {" ".join(chessboard[1])} |                   │                             │
                6. | {" ".join(chessboard[2])} |                   │    1. Help                  │ 
                5. | {" ".join(chessboard[3])} |                   │    2. Back to game          │
                4. | {" ".join(chessboard[4])} |                   │    3. Return to main menu   │
                3. | {" ".join(chessboard[5])} |                   │                             │                                         
                2. | {" ".join(chessboard[6])} |                   └─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘                              
                1. | {" ".join(chessboard[7])} |                                                                           
                    -----------------
                     a b c d e f g h
            
            

=============================================================================================================   
    """)  


def print_solve_problem_help():
    """Print the help command in the solving mode."""

    print("""
    ⇨ Solving move input format:
    
    To introduce a solution in the solving mode, follow the default syntax:
    
    The syntax includes the name of the piece which is going to be moved followed by
    the original and final position separated by a hyphen ('-').
    
    - The name of the piece is represented by its name's first capital letter in English.
    - Original and final positions are represented by their coordinates, columns from 'a'
      to 'h' and rows from '1' to '8'.

    · Remember:

        ♖ R Rook ♜ - ♘ N Knight ♞ - ♗ B Bishop ♝ - ♕ Q Queen ♛ - ♔ K King ♚ - ♙ P Pawn ♟ 
    
    The special castling move follows the syntax '0-0' for kingside castling and '0-0-0'
    for queenside castling.
    
    Examples:
                - To move a Knight from 'g1' to 'f3' the syntax is: 'Ng1-f3'
                - To move a King from 'a1' to 'b2' the syntax is: 'Ka1-b2'
                - To move a Pawn from 'd7' to 'd8' the syntax is: 'Pd7-d8'
                - To make the special move kingside castling the syntax is: '0-0'


    In this mode there exist two commands available:
    
    - The 'Hint' command to receive help while solving the problem.
    - The 'Solution' command to receive the move solution.
    
    To introduce commands while solving mode, follow the default syntax:
    
    Examples:
                - To ask for help to solve the problem the syntax is: 'HINT' or 'H'
                - To ask for the solution of the problem the syntax is: 'SOLUTION' or 'S'.
    
    
==============================================================================================================
    """)


def print_information_header():
    """Print the header in the 'About the game' mode interface."""

    print("""
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
*                                                                                                            *
*                                                                                                            *
*  █████  ██████   █████  ██    ██ ████████   ████████ ██   ██ ███████    ██████   █████  ███    ███ ███████ *
* ██   ██ ██   ██ ██   ██ ██    ██    ██         ██    ██   ██ ██        ██       ██   ██ ████  ████ ██      *
* ███████ ██████  ██   ██ ██    ██    ██         ██    ███████ █████     ██   ███ ███████ ██ ████ ██ █████   *
* ██   ██ ██   ██ ██   ██ ██    ██    ██         ██    ██   ██ ██        ██    ██ ██   ██ ██  ██  ██ ██      *
* ██   ██ ██████   █████   ██████     ██         ██    ██   ██ ███████    ██████  ██   ██ ██      ██ ███████ *                                                         *                                                                                                            *
*                                                                                                            *
*                                                                                                            *
✬ * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ✬
    """)