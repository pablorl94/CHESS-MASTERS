"""Application module.

This module contains the code needed to execute the application correctly.

The module includes:

    - Necessary functions to develope each of the modes designed in the 
      application.
    - The main structure of 'Chess Masters' including the functions that 
      interacts with the user.
    - The executable part of the code when the module is open as a script.

Application module is the third and last part of 'Chess Masters's application. 
It is the core of the application and depends on both, Rules and Visualization 
modules to functioning.

"""



##### IMPORTS #####

from copy import deepcopy
import pickle
import pathlib
from random import choice
from sys import exit
from time import sleep

from rules import *
from visualization import *



##### FUNCTIONS: GAME MODES #####

### MODE 1: Play a game ###

def setting_classic():
    """Set the starting position in classic chess modality."""
    global pieces, game_start_setting
    pieces = []
    
    create("R", "w", "a1")
    create("N", "w", "b1")
    create("B", "w", "c1")
    create("Q", "w", "d1")
    create("K", "w", "e1")
    create("B", "w", "f1")
    create("N", "w", "g1")
    create("R", "w", "h1")
    for column in COLS:
        create("P", "w", column + "2")
        
    create("R", "b", "a8")
    create("N", "b", "b8")
    create("B", "b", "c8")
    create("Q", "b", "d8")
    create("K", "b", "e8")
    create("B", "b", "f8")
    create("N", "b", "g8")
    create("R", "b", "h8")
    for column in COLS:
        create("P", "b", column + "7")
        
    game_start_setting = deepcopy(pieces)
        

def roll(dice):
    """Simulate a random roll of a dice."""
    return choice(dice)


def fischer_draw():
    """Simulate the draw to get a fischer game starting position."""
    dice = [1, 2, 3, 4, 5, 6]
    setting = ["", "", "", "", "", "", "", ""]
    
    # Step 1 #
    number = roll(dice)
    while number > 4:
        number = roll(dice)
    else:
        setting[2 * number - 2] = "B"
    
    # Step 2 #
    number = roll(dice)
    while number > 4:
        number = roll(dice)
    else:
        setting[2 * number - 1] = "B"
    
    # Step 3 #
    number = roll(dice)
    counter = 1
    for i, piece in enumerate(setting):
        if not piece:
            if counter == number:
                setting[i] = "Q"
                break
            else:
                counter = increase(counter)
    # Step 4 #
    number = roll(dice)
    while number > 5:
        number = roll(dice)
    counter = 1
    for i, piece in enumerate(setting):
        if not piece:
            if counter == number:
                setting[i] = "N"
                break
            else:
                counter = increase(counter)
                
    # Step 5 #
    number = roll(dice)
    while number > 4:
        number = roll(dice)
    counter = 1
    for i, piece in enumerate(setting):
        if not piece:
            if counter == number:
                setting[i] = "N"
                break
            else:
                counter = increase(counter)
                
    # Step 6 #
    for i, piece in enumerate(setting):
        if not piece:
            setting[i] = "R"
            break
            
    # Step 7 #
    for i, piece in enumerate(setting):
        if not piece:
            setting[i] = "K"
            break     
            
    # Step 8 #        
    for i, piece in enumerate(setting):
        if not piece:
            setting[i] = "R"
            break
            
    return setting


def setting_fischer():
    """Set the starting position in fischer chess modality."""
    global pieces, game_start_setting
    pieces = []
    
    setting = fischer_draw()
    for piece, column in zip(setting, COLS):
        create(piece, "w", column + "1")
        create("P", "w", column + "2")
        create(piece, "b", column + "8")
        create("P", "b", column + "7")
        
    game_start_setting = deepcopy(pieces)
        
        
def get_move_notation(chess_move):
    """Return the complete notation of a given chess move."""

    if chess_move in ["0-0", "0-0-0"]:
        move_notation = chess_move
        for color in "w/b":
            if is_checkmate(color):
                move_notation += "#"
            elif is_check(color):
                move_notation += "+"         
    else:
        m_piece = chess_move[0].upper()
        m_init = chess_move[1:3].lower()
        m_ends = chess_move[4:6].lower()

        if m_piece == "P" and m_ends[-1] in "1/8":
            promoted_piece = seek_piece(m_ends).name
            move_notation = m_piece + m_init + "-" + m_ends + "=" + promoted_piece
        else:
            move_notation = m_piece + m_init + "-" + m_ends
        
        color = "w" if seek_piece(m_ends).color == "b" else "b"
        if is_checkmate(color):
            move_notation += "#"
        elif is_check(color):
            move_notation += "+"
            
    return move_notation


def is_format_correct(move_input):
    """Verify if the user's move input is correct according to its format."""

    if move_input in ["0-0", "0-0-0"]:
        return True
    if len(move_input) != 6:
        return False
    
    piece_cond = move_input[0].upper() in "RNBQKP"
    move1_cond = move_input[1].lower() in COLS and move_input[2] in ROWS
    sign_cond = move_input[3] == "-"
    move2_cond = move_input[4].lower() in COLS and move_input[5] in ROWS
    
    return True if all([piece_cond, move1_cond, sign_cond, move2_cond]) else False

    

def is_move_correct(move_input, color):
    """Verify if the user's move is correct according to chess rules."""
    
    color_name = "white" if color == "w" else "black"
    m_piece = move_input[0].upper()
    m_init = move_input[1:3].lower()
    m_ends = move_input[4:6].lower()
    
    piece = seek_piece(m_init)
    if not piece:
        print(f"It is an invalid move. There is no a piece in '{m_init}'.", end="\n\n")
        return False
    elif piece.name != m_piece:
        print(f"It is an invalid move. There is no a '{m_piece}' in '{m_init}'.", end="\n\n")
        return False
    elif piece.color != color:
        print(f"It is an invalid move. It is {color_name}'s turn.", end="\n\n")
        return False
    elif is_check(color) and \
         (m_piece, m_init, m_ends) not in check_allowed_movements(color):
        print("It is an invalid move. It's check!", end= "\n\n")
        return False
    elif not is_check(color) and \
         (m_piece, m_init, m_ends) not in check_allowed_movements(color):
        print(f"It is an invalid move. It is not allowed to move {move_input}.", end="\n\n")
        return False
    else:
        return True
    
    
def save_game():
    """Save a game in pickle format."""
    print()
    file_name = input(">> Introduce a name for the game: ")
    sleep(1)
    print()
    white_player = input(">> Introduce the name of the player with white pieces: ")
    sleep(1)
    print()
    black_player = input(">> Introduce the name of the player with black pieces: ")
    sleep(1)
    print()
    tournament_year = input(">> Introduce the name and date of the tournament where the game took place: ")
    sleep(1)
    print()
    print("    Result format: '1-0', '1/2-1/2' or '0-1'", end="\n\n")
    repeat = True
    while repeat:
        result = input(">> Introduce the result of the game (optional): ")
        sleep(1)
        if result in ["1-0", "0-1", "1/2-1/2"]:
            result = [result.split("-")[0].center(3), result.split("-")[1].center(3)]
            break
        elif result == "":
            break
        
    game_info = {"white_player": white_player, 
                 "black_player": black_player, 
                 "tournament_year": tournament_year, 
                 "starting_position": game_start_setting, 
                 "notation": notation,
                 "result": result}
    
    with open(file_name + ".pickle", "wb") as file:
        pickle.dump(game_info, file)


def load_game(game_name):
    """Load a saved game. The 'game_name' argument is the file name WITHOUT the extension '.pickle'."""
    file_name = game_name + ".pickle"
    for item in pathlib.Path(".").iterdir():
        if file_name == item.name and item.is_file():
            with open(file_name, "rb") as file:
                game_info = pickle.load(file)
            return game_info
    else:
        print("Invalid file name. Please try again.")
    
    
def execute_in_game_options(setting=False):
    """Execute in game options menu in playing mode."""

    while True:
        screen_reset()
        print_set_and_play_header() if setting else print_play_game_header()
        print_play_game_options(pieces)
        option = input(">> Introduce the number of the command you want to execute: ")
        sleep(2)
        print()
        
        if option not in ["1", "2", "3", "4"]:
            print("Remember, only numbers from 1 to 4 are accepted. Please, try again.", end="\n\n")
            sleep(3)
            continue
            
        if option == "1":
            print("You have selected the first option: Help command.", end="\n\n")
            sleep(2)
            print_play_game_help()
            sleep(3)
            input("Press any key to continue: ")
            
        elif option == "2":
            print("You have selected the second option: Save the game command.", end="\n\n")
            sleep(2)
            print(">> Do you want to save your game?", end="\n\n")
            select = input("Select 'YES' to save your game and 'NO' otherwise: ")
            sleep(2)
            if select.upper() in ["YES", "Y"]:
                save_game()
            
        elif option == "3":
            print("You have selected the third option: Back to game.", end="\n\n")
            sleep(2)
            break
            
        elif option == "4":
            print("You have selected the fourth option: Return to main menu.", end="\n\n")
            sleep(2)
            print(">> Are you sure do you want to return to menu?", end="\n\n")
            select = input("Select 'YES' to return to main menu and 'NO' otherwise: ")
            if select.upper() in ["YES", "Y"]:
                print()
                print(">> Do you want to save your game before returning to menu?", end="\n\n")
                select = input("Select 'YES' to save your game and 'NO' otherwise: ")
                if select.upper() in ["YES", "Y"]:
                    save_game()
                sleep(3)
                execute_main_menu()


def player_turn(color, notation, setting=False):
    """Reproduce the sequence of the player turn for a color."""
    
    turn = 0 if color == "w" else 1
    color_name = "white" if color == "w" else "black"
    chess_move = input(f">> Introduce a move for the {color_name} pieces: ")
    print()
    
    if chess_move.upper() == "OPTIONS":
        print("You have selected the Options command.", end= "\n\n")
        sleep(3)
        execute_in_game_options(setting=setting)

    elif is_format_correct(chess_move):
        if chess_move == "0-0":
            castle = "kingside"
            for piece in pieces:
                if piece.color == color and piece.name == "K":
                    king = piece
                    if king.castling_move(castle):
                        print("Kingside castling.", end= "\n\n")
                        king.move("0-0")
                        notation[turn].append(get_move_notation(chess_move))
                    else:
                        print("Invalid castling movement.", end= "\n\n")

        elif chess_move == "0-0-0":
            castle = "queenside"
            for piece in pieces:
                if piece.color == color and piece.name == "K":
                    king = piece
                    if king.castling_move(castle):
                        print("Queenside castling.", end= "\n\n")
                        king.move("0-0-0")
                        notation[turn].append(get_move_notation(chess_move))
                    else:
                        print("Invalid castling movement.", end= "\n\n")

        else:
            m_init = chess_move[1:3].lower()
            m_ends = chess_move[4:6].lower()
            piece = seek_piece(m_init)
            if is_move_correct(chess_move, color):    
                piece.move(m_ends)
                notation[turn].append(get_move_notation(chess_move))
                
    else:
        print("Invalid input syntax. Please, try again.", end= "\n\n")


def cpu_turn(color, notation):
    """Reproduce the sequence of the CPU turn for a color."""
    turn = 0 if color == "w" else 1
    chess_move = choice(check_allowed_movements(color))
    piece = seek_piece(chess_move[1])
    piece.move(chess_move[2])
    chess_move = chess_move[0] + chess_move[1] + "-" + chess_move[2]
    notation[turn].append(get_move_notation(chess_move))


def fifty_moves_draw_rule(moves_counter):
    """Check the fifty moves draw chess rule."""
    return True if moves_counter >= 100 else False

    
def comment_move():
    """Introduce a comment."""
    return input(">> Introduce a comment to the move: ")
    

def play(w_player="player", b_player="cpu", turn = "w", setting=False):
    """Reproduce the sequence of a chess game."""
    global notation
    notation = [["White"], ["Black"]]
    
    if turn == "b":
        notation[0].append("...")
    
    # Fifty Moves Draw Rule.
    moves_counter, pieces_counter = 0, len(pieces)
    
    screen_reset()
    print_set_and_play_header() if setting else print_play_game_header()
    print_play_game_playing(pieces, notation)
    
    while True:
        color_turn = "w" if len(notation[0]) <= len(notation[1]) else "b"
        color_num = 0 if color_turn == "w" else 1
        
        # Fifty Moves Draw Rule.
        if len(pieces) == pieces_counter:
            moves_counter = increase(moves_counter)
        else:
            moves_counter, pieces_counter = 0, len(pieces) 
        
        if is_checkmate(color_turn):
            result = [" 1 ", " 0 "] if color_turn == "b" else [" 0 ", " 1 "]
            screen_reset()
            print_set_and_play_header() if setting else print_play_game_header()
            print_play_game_playing(pieces, notation, result)
            print("Checkmate!")
            sleep(5)
            print()
            print(">> Do you want to save your game before returning to menu?", end="\n\n")
            select = input("Select 'YES' to save your game and 'NO' otherwise: ")
            if select.upper() in ["YES", "Y"]:
                save_game()
            sleep(3)
            execute_main_menu()
            break
            
        elif is_stalemate(color_turn):
            result = ["1/2", "1/2"]
            screen_reset()
            print_set_and_play_header() if setting else print_play_game_header()
            print_play_game_playing(pieces, notation, result)
            print("Stalemate...")
            sleep(5)
            print()
            print(">> Do you want to save your game before returning to menu?", end="\n\n")
            select = input("Select 'YES' to save your game and 'NO' otherwise: ")
            if select.upper() in ["YES", "Y"]:
                save_game()
            sleep(3)
            execute_main_menu()
            break
            
        elif fifty_moves_draw_rule(moves_counter):
            result = ["1/2", "1/2"]
            screen_reset()
            print_set_and_play_header() if setting else print_play_game_header()
            print_play_game_playing(pieces, notation, result)
            print("Fifty moves draw rule. It's draw.")
            sleep(5)
            print()
            print(">> Do you want to save your game before returning to menu?", end="\n\n")
            select = input("Select 'YES' to save your game and 'NO' otherwise: ")
            if select.upper() in ["YES", "Y"]:
                save_game()
            sleep(3)
            execute_main_menu()
            break
            
        if is_check(color_turn):
            print("Check!", end= "\n\n")
            
        if [w_player, b_player][color_num] == "cpu":
            cpu_turn(color_turn, notation)
        else:
            player_turn(color_turn, notation, setting=setting)
            
        sleep(2)
        screen_reset()
        print_set_and_play_header() if setting else print_play_game_header()
        print_play_game_playing(pieces, notation)


def play_game(game_modality, opponent="cpu", user_color="w"):
    """The main function for the 'Play a game' mode."""
    
    setting_classic() if game_modality == "classic" else setting_fischer()
        
    if opponent == "cpu":
        w_player = "player" if user_color == "w" else "cpu"
        b_player = "player" if user_color == "b" else "cpu"
    else:
        w_player, b_player = "player", "player"    
        
    play(w_player=w_player, b_player=b_player)


        
### MODE 2: Set and Play ###
      
def is_setting_format_correct(piece_input):
    """Verify if the piece input format is correct in setting mode."""
    if len(piece_input) != 5:
        return False
    piece_name_cond = piece_input[0].upper() in "RNBQKP"
    piece_color_cond = piece_input[1].lower() in "wb"
    sign_cond = piece_input[2] == "-"
    position_cond = piece_input[3].lower() in COLS and piece_input[4] in ROWS
    if all([piece_name_cond, piece_color_cond, sign_cond, position_cond]):
        return True
    else:
        return False


def is_setting_position_correct(turn):
    """Verify if the introduced position is correct in setting mode."""
    global pieces
    white_king, black_king = False, False
    king_counter = 0
    print()
    for piece in pieces:
        if piece.name == "P":
            if piece.position[-1] in "1/8":
                print("Remember, pawns cannot be in first or last row.", end="\n\n")
                return False
        if piece.name == "K":
            if piece.color == "w":
                white_king = True
                king_counter = increase(king_counter)
            elif piece.color == "b":
                black_king = True
                king_counter = increase(king_counter)
    if white_king and black_king:
        if king_counter != 2:
            print("Invalid position. There cannot be more than two kings on the board.", end="\n\n")
            return False
        elif is_check("w") and is_check("b"):
            print("Invalid position. Both kings cannot be in check.", end="\n\n")
            return False
        elif is_check("w") and turn != "w" or is_check("b") and turn != "b":
            print("Invalid position. King cannot be in check while opponent's turn.", end="\n\n")
            return False
        else:
            return True
    else:
        print("Invalid position. Must be both kings on the board.", end="\n\n")
        return False


def setting_position():
    """Define the position in setting mode."""
    global pieces, game_start_setting, setting_notation
    pieces, setting_notation = [], [["White"], ["Black"]]
    
    repeat = True
    while repeat:
        screen_reset()
        print_set_and_play_header()
        print_set_and_play_setting(pieces, setting_notation)
        piece_input = input(">> Introduce a piece into the board: ")
        if piece_input == "":
            print()
            sleep(2)
            break
        elif piece_input.upper() == "OPTIONS":
            print()
            print("You have selected the Options command.", end= "\n\n")
            sleep(3)
            execute_setting_options()
        elif is_setting_format_correct(piece_input) and \
             not seek_piece(piece_input[3:5]):
            piece_input = piece_input[0].upper() + piece_input[1:].lower()
            create(piece_input[0], piece_input[1], piece_input[3:5])
            if piece_input[1].lower() == "w":
                setting_notation[0].append(get_print_setting_notation(piece_input))
            else:
                setting_notation[1].append(get_print_setting_notation(piece_input))
            
            screen_reset()
            print_set_and_play_header()    
            print_set_and_play_setting(pieces, setting_notation)
            
        else:
            print()
            print("Invalid input format. Please try again.", end= "\n\n")
            sleep(3)
            
    game_start_setting = deepcopy(pieces)
    

def ask_turn():
    """Ask which color turn is it."""
    while True:
        screen_reset()
        print_set_and_play_header()    
        print_set_and_play_setting(pieces, setting_notation)
        
        color_turn = input(">> Introduce the color that is going to play first (w/b): ")
        if color_turn.lower() == "w" or color_turn == "":
            return "w"
        elif color_turn.lower() == "b":
            return "b"
        else:
            sleep(1)
            print()
            print("Invalid input. Remember only 'w' or 'b' are valid inputs.")
            sleep(2)
            

def ask_options_setting():
    """Ask for the opponent and color to play with in setting mode."""
    while True:
        screen_reset()
        print_set_and_play_header()    
        print_set_and_play_setting(pieces, setting_notation)
        
        print(">> Do you want to play 'vs player' or 'vs CPU'?")
        print()
        opponent = input(">> Introduce PLAYER to play with a friend or CPU to match the machine (default): ")
        if opponent.lower() == "player":
            opponent = "player"
            break
        elif opponent.lower() == "cpu" or opponent == "":
            opponent = "cpu"
            break
        else:
            print()
            print("Invalid input syntax. Please, only PLAYER and CPU are available inputs.")
        sleep(3)
            
    if opponent == "cpu":
        while True:
            screen_reset()
            print_set_and_play_header()    
            print_set_and_play_setting(pieces, setting_notation)
            
            print(f">> You're playing 'vs {opponent}', do you prefer to play with white pieces or black pieces?")
            print()
            user_color = input(">> Introduce WHITE to play with white pieces (default) or BLACK to play with the black ones: ")
            if user_color.lower() in ["white", "w", ""]:
                user_color = "w"
                break
            elif user_color.lower() in ["black", "b"]:
                user_color = "b"
                break
            else:
                print()
                print("Invalid input syntax. Please, only WHITE and BLACK are available inputs.")
                sleep(2)
    else:
        user_color = "w"
            
    return opponent, user_color


def execute_setting_options():
    """Execute in game options menu in setting mode."""
    while True:
        screen_reset()
        print_set_and_play_header()    
        print_set_and_play_options(pieces)
        
        option = input(">> Introduce the number of the command you want to execute: ")
        sleep(2)
        print()
        
        if option not in ["1", "2", "3"]:
            print("Remember, only numbers from 1 to 3 are accepted. Please, try again.", end="\n\n")
            sleep(3)
            continue
            
        if option == "1":
            print("You have selected the first option: Help command.", end="\n\n")
            sleep(2)
            print_set_and_play_help()
            sleep(3)
            input("Press any key to continue: ")
            
        elif option == "2":
            print("You have selected the second option: Back to game.", end="\n\n")
            sleep(3)
            break
            
        elif option == "3":
            print("You have selected the third option: Return to main menu.", end="\n\n")
            sleep(3)
            print(">> The position will be lost. Are you sure do you want to return to menu?", end="\n\n")
            select = input("Select 'YES' to return to main menu and 'NO' otherwise: ")
            if select.upper() in ["YES", "Y"]:
                sleep(3)
                execute_main_menu()


def set_and_play():
    """The main function for the 'Set and play' game mode."""
    setting_position()
    color_turn = ask_turn()
    sleep(2)
    if is_setting_position_correct(color_turn):
        opponent, user_color = ask_options_setting()
        if opponent == "cpu":
            w_player = "player" if user_color == "w" else "cpu"
            b_player = "player" if user_color == "b" else "cpu"
        else:
            w_player, b_player = "player", "player"
        sleep(2)
        play(w_player=w_player, b_player=b_player, turn=color_turn, setting=True)
    else:
        again = input(">> Do you want to set the board again? YES/NO: ")
        if again.upper() in ["Y", "YES"]:
            sleep(2)
            set_and_play()
        else:
            sleep(2)
            print()
            print("Returning to main menu...")
            sleep(3)
            execute_main_menu()

                   
            
### MODE 3: Analyze a game ###

def create_move_list(chess_notation):
    """Create a list which includes game's chess moves as elements."""
    move_list = []
    turn = "b" if chess_notation[0][0] == "..." else "w"
    if len(chess_notation[0]) > len(chess_notation[1]):
        chess_notation[1].append("...")
    for w_move, b_move in zip(chess_notation[0], chess_notation[1]):
        if w_move.upper() != "WHITE" and b_move.upper() != "BLACK":
            move_list.append(w_move)
            move_list.append(b_move)
    while "..." in move_list:
        move_list.remove("...")
    return (move_list, turn)


def reproduce_game(starting_position, turn, move_list, move_counter, players, tournament, result, solving=False):
    """Reproduces a game from its starting position to a determined move.

    Arguments:

    starting_position -- the starting position of the game.
    turn -- the color which is going to play first.
    move_list -- a list with the moves of the game.
    move counter -- the last move in notation which is going to be reproduced.
    result -- the result of the game.
    solving (optional) -- 'True' if it is solving a problem. By default 'False'
    """
    global pieces
    pieces = deepcopy(starting_position)
    other = "b" if turn == "w" else "w"
    chess_notation = [["White"], ["Black"]]
    
    for i, move in enumerate(move_list):
        color = 0 if turn == "w" else 1
        if i < move_counter:
            if move[:5] == "0-0-0":
                if turn == "w":
                    seek_piece("e1").set_position("c1")
                    seek_piece("a1").set_position("d1")
                elif turn == "b":
                    seek_piece("e8").set_position("c8")
                    seek_piece("a8").set_position("d8")
                chess_notation[color].append(move)
            
            elif move[:3] == "0-0":
                if turn == "w":
                    seek_piece("e1").set_position("g1")
                    seek_piece("h1").set_position("f1")
                elif turn == "b":
                    seek_piece("e8").set_position("g8")
                    seek_piece("h8").set_position("f8")
                chess_notation[color].append(move)
                    
            else:
                m_piece = move[0].upper()
                m_init = move[1:3].lower()
                m_ends = move[4:6].lower()

                piece = seek_piece(m_init)
                if seek_piece(m_ends):
                    pieces.remove(seek_piece(m_ends))
                piece.set_position(m_ends)

                if m_piece == "P" and m_ends[-1] in "1/8":
                    create(move[7], piece.color, piece.position)
                    pieces.remove(piece)
                
                chess_notation[color].append(move)
            turn, other = other, turn
        else:
            break
            
    result = result if (result and move_counter == len(move_list)) else None
    
    screen_reset()
    print_solve_problem_header() if solving else print_analyze_game_header()
    if solving:
        print_solve_problem_playing(pieces, notation, players, tournament, result)
    else: 
        print_analyze_game_playing(pieces, chess_notation, players, tournament, result)
    
    
def execute_analyzing_options():
    """Execute in game options menu in analyzing mode."""
    while True:
        screen_reset()
        print_analyze_game_header()    
        print_analyze_game_options(pieces)
        
        option = input(">> Introduce the number of the command you want to execute: ")
        sleep(2)
        print()
        
        if option not in ["1", "2", "3"]:
            print("Remember, only numbers from 1 to 3 are accepted. Please, try again.", end="\n\n")
            sleep(3)
            continue
            
        if option == "1":
            print("You have selected the first option: Help command.", end="\n\n")
            sleep(2)
            print_analyze_game_help()
            sleep(3)
            input("Press any key to continue: ")
            
        elif option == "2":
            print("You have selected the second option: Back to game.", end="\n\n")
            sleep(3)
            break
            
        elif option == "3":
            print("You have selected the third option: Return to main menu.", end="\n\n")
            sleep(3)
            print(">> Are you sure do you want to return to menu?", end="\n\n")
            select = input("Select 'YES' to return to main menu and 'NO' otherwise: ")
            if select.upper() in ["YES", "Y"]:
                sleep(3)
                execute_main_menu()    


def analyze_game(game_name):
    """The main function for the 'Analyze a game' game mode."""
    global pieces, notation
    g_info = load_game(game_name)
    move_list, turn = create_move_list(g_info["notation"])
    move_counter = 0
    
    pieces = g_info["starting_position"]
    notation = g_info["notation"]
    players = [g_info["white_player"], g_info["black_player"]] 
    tournament = g_info["tournament_year"]
    result = g_info["result"]
    
    reproduce_game(g_info["starting_position"], turn, move_list, move_counter, players, tournament, result)
    
    repeat = True
    while repeat:
        print(">> What would you like to do?", end="\n\n")
        option = input("Select an option - Next(N)/Back(B): ")
        option = option.upper()
        sleep(1)
        if option == "OPTIONS":
            print()
            print("You have selected the Options command.", end= "\n\n")
            sleep(3)
            execute_analyzing_options()
        
        elif option not in ["NEXT", "N", "BACK", "B"]:
            print()
            print("Remember, only 'N' (next) and 'B' (back) are valid options.", end="\n\n")
            sleep(2)
        else:
            if option.upper() == "N" and move_counter != len(move_list):
                move_counter = increase(move_counter, 1)
                reproduce_game(
                    g_info["starting_position"], 
                    turn, move_list, 
                    move_counter, 
                    players,
                    tournament,
                    result)
            elif option.upper() == "N":
                print()
                print("It is not possible to move forward. The game has ended!", end="\n\n")
                sleep(2)
            elif option.upper() == "B" and move_counter != 0:
                move_counter = increase(move_counter, -1)
                reproduce_game(
                    g_info["starting_position"], 
                    turn, move_list, 
                    move_counter, 
                    players,
                    tournament,
                    result)
            elif option.upper() == "B":
                print()
                print("It is not possible to move back. It is the starting position!", end="\n\n")
                sleep(2)


                
### MODE 4: Solve a problem ###
    
def execute_solving_options():
    """Execute in game options menu in solving mode."""
    while True:
        screen_reset()
        print_solve_problem_header()    
        print_solve_problem_options(pieces)
        
        option = input(">> Introduce the number of the command you want to execute: ")
        sleep(2)
        print()
        
        if option not in ["1", "2", "3"]:
            print("Remember, only numbers from 1 to 3 are accepted. Please, try again.", end="\n\n")
            sleep(3)
            continue
            
        if option == "1":
            print("You have selected the first option: Help command.", end="\n\n")
            sleep(2)
            print_solve_problem_help()
            sleep(3)
            input("Press any key to continue: ")
            
        elif option == "2":
            print("You have selected the second option: Back to game.", end="\n\n")
            sleep(3)
            break
            
        elif option == "3":
            print("You have selected the third option: Return to main menu.", end="\n\n")
            sleep(3)
            print(">> Are you sure do you want to return to menu?", end="\n\n")
            select = input("Select 'YES' to return to main menu and 'NO' otherwise: ")
            if select.upper() in ["YES", "Y"]:
                sleep(3)
                execute_main_menu()    
    
                
def solve_problem(problem_name):
    """The main function for the 'Solve a problem' game mode."""
    global pieces, notation
    g_info = load_game(problem_name)
    move_list, turn = create_move_list(g_info["notation"])
    move_counter = 0
    
    pieces = g_info["starting_position"]
    notation = g_info["notation"]
    players = [g_info["white_player"], g_info["black_player"]] 
    tournament = g_info["tournament_year"]
    result = g_info["result"]
    
    color = "white" if turn == "w" else "black"
    playing = "player"
    
    repeat = True
    while repeat:

        screen_reset()
        print_solve_problem_header()
        reproduce_game(pieces, turn, move_list, move_counter, players, tournament, result, solving=True)

        if move_counter == len(move_list):
            print("Congratulations! The problem is solved.", end="\n\n")
            sleep(2)
            input("Press any key to continue: ")
            print()
            sleep(1)
            print("Returning to main menu...")
            sleep(3)
            execute_main_menu()
        
        if playing == "player":
            option = input(f">> Introduce your move for {color} pieces: ")
            option = option
            sleep(2)
            print()
            
            if option.upper() == "OPTIONS":
                print("You have selected the Options command.", end= "\n\n")
                sleep(3)
                execute_solving_options()
            
            elif option.upper() in ["H", "HINT"]:
                print("You have selected the Hint command.", end= "\n\n")
                sleep(3)
                print(f"Listen carefully: It appears that {move_list[move_counter][:3]} wants to be moved...", end="\n\n")
                sleep(5)
                
            elif option.upper() in ["S", "SOLUTION"]:
                print("You have selected the Solution command.", end= "\n\n")
                sleep(3)
                if "0-0-0" in move_list[move_counter]:
                    solution = "0-0-0"
                elif "0-0" in move_list[move_counter]:
                    solution = "0-0"
                elif move_list[move_counter][0] == "P" and \
                     move_list[move_counter][5] in "1/8":
                    piece_to_promote = move_list[move_counter][:6]
                    promote_piece = move_list[move_counter][7]
                    solution = piece_to_promote + " promoting to " + promote_piece
                else:
                    solution = move_list[move_counter][:6]
                    
                print(f"The solution is: {solution}.", end="\n\n")
                sleep(5)
                
            else:
                if is_format_correct(option):
                    if option in move_list[move_counter]:
                        if move_list[move_counter][0] == "P" and \
                           move_list[move_counter][5] in "1/8":
                            promoted = input(">> Introduce the piece you want to promote to: ")
                            print()
                            if promoted in ["R", "N", "B", "Q"]:
                                if promoted != move_list[move_counter][7]:
                                    print("The input move isn't the best in this position. Please try again.", end="\n\n")
                                    continue
                            else:
                                print("Only R/N/B/Q can be promoted. Please try again.", end="\n\n")
                                continue
                        move_counter = increase(move_counter)
                        playing = "cpu"
                    else:
                        print("The input move isn't the best in this position. Please try again.", end="\n\n")
                else:
                    print("Invalid input syntax. Please try again.", end="\n\n")
                    continue
                    
        else:
            move_counter = increase(move_counter)
            playing = "player"



### MODE 5: About the game ###

def print_about_game():
    """The main function for the 'About the game' game mode."""

    print("""

    The application 'Chess Masters' has been developed by Pablo Rodriguez Lapetra 
    as an academic final project for the Master in Programming with Python of 'Cice,
    la Escuela Profesional de Nuevas Tecnologías' imparted by Jorge Lopez Arienza.

                        ♙ ♟   ♙ ♟   ♙ ♟   ♙ ♟   ♙ ♟   ♙ ♟ 
    
    The original idea was to program a small app to be able to play chess games on 
    the Python shell in an improvised chessboard according to chess rules.
    
    Today, the app includes many more functionalities and a lot of ideas to keep it
    growing up in the near future.

                        ♙ ♟   ♙ ♟   ♙ ♟   ♙ ♟   ♙ ♟   ♙ ♟ 
    
    I've been playing chess since a long time ago. I love chess and I'm glad to share 
    with you this small part of me.
    

    I hope you like it!
                                                                 Madrid, 2020
                                                             The author, P♔blo :)
    
    
===========================================================================================================
    """)



##### FUNCTIONS: GAME STRUCTURE #####

### MAIN MENU ###

def reset_main_menu_interface():
    """Reset main menu's interface."""
    screen_reset()
    print_main_interface()

def execute_main_menu():
    """Execute the main menu."""
    while True:
        reset_main_menu_interface()
        option = input(">> Introduce the number of the game mode you want to play: ")
        print()
        
        if option not in ["1", "2", "3", "4", "5", "6"]:
            reset_main_menu_interface()
            print("Remember, only numbers from 1 to 6 are accepted. Please, try again.", end="\n\n")
            sleep(3)
            continue
            
        if option == "1":
            reset_main_menu_interface()
            print("You have selected the first option: Play a game.", end="\n\n")
            sleep(3)
            execute_play_game_mode()
            
        elif option == "2":
            reset_main_menu_interface()
            print("You have selected the second option: Set and play.", end="\n\n")
            sleep(3)
            execute_set_and_play_mode()
            
        elif option == "3":
            reset_main_menu_interface()
            print("You have selected the third option: Analyze a game.", end="\n\n")
            sleep(3)
            execute_analyze_game_mode()
            
        elif option == "4":
            reset_main_menu_interface()
            print("You have selected the fourth option: Solve a problem.", end="\n\n")
            sleep(3)
            execute_solve_problem_mode()
            
        elif option == "5":
            reset_main_menu_interface()
            print("You have selected the fifth option: About the game.", end="\n\n")
            sleep(3)
            screen_reset()
            print_information_header()
            print_about_game()
            input("Press any key to continue: ")
            continue
            
        elif option == "6":
            sleep(1)
            print("I hope you've spent a great time. See you soon!")
            sleep(3)
            exit(0)


### PLAY A GAME ###

def reset_play_game_mode_interface():
    """Reset menu's interface in the 'Play a game' mode."""
    screen_reset()
    print_play_game_header()
    print_play_game_menu()
    

def print_play_game_mode_info():
    """Print the information about 'Play a game' mode."""

    print("""
    In this mode you'll be able to play a chess game. 
    
    The mode includes two modalities, 'Classic' and 'Fischer':
    
        ♙ In 'Classic' modality you'll find a classic chess game, where the starting 
          position and rules are the typical in chess.
    
        ♟ In 'Fischer' modality rules are the same but the starting position is set 
          at random, so every game may be different than the previous!
    
    Both modalities include the possibility of playing with a friend or the CPU.
    Dont worry if the CPU is too bad at chess... It is still learning!
    

===========================================================================================================  
    """)
    
    
def ask_options():
    """Ask for the opponent and color to play with in 'Play a game' mode."""
    while True:
        reset_play_game_mode_interface()
        print(">> Do you want to play 'vs player' or 'vs CPU'?")
        print()
        opponent = input(">> Introduce PLAYER to play with a friend or CPU to match the machine (default): ")
        if opponent.lower() == "player":
            opponent = "player"
            break
        elif opponent.lower() == "cpu" or opponent == "":
            opponent = "cpu"
            break
        else:
            print()
            print("Invalid input syntax. Please, only PLAYER and CPU are available inputs.")
            sleep(3)
            
    if opponent == "cpu":
        while True:
            reset_play_game_mode_interface()
            print(f">> You're playing 'vs {opponent}', do you prefer to play with white pieces or black pieces?")
            print()
            user_color = input(">> Introduce WHITE to play with white pieces (default) or BLACK to play with the black ones: ")
            if user_color.lower() in ["white", "w", ""]:
                user_color = "w"
                break
            elif user_color.lower() in ["black", "b"]:
                user_color = "b"
                break
            else:
                print()
                print("Invalid input syntax. Please, only WHITE and BLACK are available inputs.")
                sleep(3)
    else:
        user_color = "w"
            
    return opponent, user_color
    

def execute_play_game_mode():
    """Execute the menu in 'Play a game' mode."""
    while True:
        reset_play_game_mode_interface()
        option = input(">> Introduce the number of the game mode you want to access: ")
        print()
        
        if option not in ["1", "2", "3", "4"]:
            reset_play_game_mode_interface()
            print("Remember, only numbers from 1 to 4 are accepted. Please, try again.", end="\n\n")
            sleep(3)
            continue
            
        if option == "1":
            reset_play_game_mode_interface()
            print("You have selected the first option: Information about the mode.", end="\n\n")
            sleep(3)
            screen_reset()
            print_play_game_header()
            print_play_game_mode_info()
            input("Press any key to continue: ")
            continue
            
        elif option == "2":
            reset_play_game_mode_interface()
            print("You have selected the second option: Play a Classic game.", end="\n\n")
            sleep(3)
            opponent, user_color = ask_options()
            sleep(3)
            play_game("classic", opponent=opponent, user_color=user_color)
            
            
        elif option == "3":
            reset_play_game_mode_interface()
            print("You have selected the third option: Play a Fischer game.", end="\n\n")
            sleep(3)
            opponent, user_color = ask_options()
            sleep(3)
            play_game("fischer", opponent=opponent, user_color=user_color)
            
        elif option == "4":
            reset_play_game_mode_interface()
            print("You have selected the fourth option: Return to main menu.", end="\n\n")
            sleep(3)
            execute_main_menu()


### SET AND PLAY ###

def reset_set_and_play_mode_interface():
    """Reset menu's interface in the 'Set and play' mode."""
    screen_reset()
    print_set_and_play_header()
    print_set_and_play_menu()
    
    
def print_set_and_play_mode_info():
    """Print the information about 'Set and play' mode."""

    print("""
    In this mode you'll be able to set a position and play it according to cl♔ssic 
    chess rules. 
    
    The mode is developed in two parts:
    
        ♙ In the first part, you'll be able to define the position before playing.
          Some restrictions are considered here. Don't try to play with two kings!! 
    
        ♟ The second part is funnier. You'll be playing your customized position!
    
    In both cases, the game will follow classic chess rules and gives the possibility 
    of playing with a friend or the CPU. Be patient if the CPU is too bad at the 
    beginning... It has a great potent♝al!
    

===========================================================================================================  
    """)    
    

def execute_set_and_play_mode():
    """Execute the menu in 'Set and play' mode."""
    while True:
        reset_set_and_play_mode_interface()
        option = input(">> Introduce the number of the game mode you want to access: ")
        print()
        
        if option not in ["1", "2", "3"]:
            reset_set_and_play_mode_interface()
            print("Remember, only numbers from 1 to 4 are accepted. Please, try again.", end="\n\n")
            sleep(3)
            continue
            
        if option == "1":
            reset_set_and_play_mode_interface()
            print("You have selected the first option: Information about the mode.", end="\n\n")
            sleep(3)
            screen_reset()
            print_set_and_play_header()
            print_set_and_play_mode_info()
            input("Press any key to continue: ")
            continue
            
        elif option == "2":
            reset_set_and_play_mode_interface()
            print("You have selected the second option: Set and play a game.", end="\n\n")
            sleep(3)
            set_and_play()
            
        elif option == "3":
            reset_set_and_play_mode_interface()
            print("You have selected the third option: Return to main menu.", end="\n\n")
            sleep(3)
            execute_main_menu()


### ANALYZE A GAME ###

def reset_analyze_game_mode_interface():
    """Reset menu's interface in the 'Analyze a game' mode."""
    screen_reset()
    print_analyze_game_header()
    print_analyze_game_menu()
    
    
def print_analyze_game_mode_info():
    """Print the information about 'Analyze a game' mode."""

    print("""
    In this mode you'll be able to reproduce a game.
    
    The game can be an historic match between two Masters of chess or one of
    your games saved before. Everything is reproduced here! ♔ ♚
    
    Analyzing a game is perfect for players who want to improve their level.
    It is also valid if you want to share your games with friends or remind 
    how you destroyed the machine... Do ♝t before it is too late.
    
        ♜ Considerations: Chess games must be in your directory with a Python 
          '.pickle' extension to be reproduced. 


===========================================================================================================  
    """)       
    

def execute_analyze_game_mode():
    """Execute the menu in 'Analyze a game' mode."""
    while True:
        reset_analyze_game_mode_interface()
        option = input(">> Introduce the number of the game mode you want to access: ")
        print()
        
        if option not in ["1", "2", "3"]:
            reset_analyze_game_mode_interface()
            print("Remember, only numbers from 1 to 3 are accepted. Please, try again.", end="\n\n")
            sleep(3)
            continue
            
        if option == "1":
            reset_analyze_game_mode_interface()
            print("You have selected the first option: Information about the mode.", end="\n\n")
            sleep(3)
            screen_reset()
            print_analyze_game_header()
            print_analyze_game_mode_info()
            input("Press any key to continue: ")
            continue
            
        elif option == "2":
            reset_analyze_game_mode_interface()
            print("You have selected the second option: Analyze a game.", end="\n\n")
            sleep(3)
            while True:
                print(">> Introduce the name of the file you want to reproduce.", end="\n\n")
                file_name = input("Remember! Introduce the name of the file without '.pickle' extension.")
                for item in pathlib.Path(".").iterdir():
                    if (file_name + ".pickle") == item.name and item.is_file():
                        analyze_game(file_name)
                else:
                    print()
                    print("The name introduced cannot be reproduced as a chess game.", end="\n\n")
                    sleep(3)
                repeat = input("Do you want to try again? Select 'YES'/'NO': ")
                if repeat.upper() not in ["YES", "Y"]:
                    break
            
        elif option == "3":
            reset_analyze_game_mode_interface()
            print("You have selected the third option: Return to main menu.", end="\n\n")
            sleep(3)
            execute_main_menu()


### SOLVE A PROBLEM ###

def reset_solve_problem_mode_interface():
    """Reset menu's interface in the 'Play a game' mode."""
    screen_reset()
    print_solve_problem_header()
    print_solve_problem_menu()
    
    
def print_solve_problem_mode_info():
    """Print the information about 'Solve a problem' mode."""

    print("""
    In this mode you'll be able to solve different chess problems.
    
    I've prepared a challenge for you: Great problems to solve! ♘
    
    There are problems from different levels of difficulty. Some of them are
    taken from existing games. Others are studies... Try to solve them all!
    
    If you don't find a solution don't despair, just ask for ♛ hint. 
    
        ♖ Considerations: Chess problems must be in your directory with a Python 
          '.pickle' extension to be reproduced. 
 

===========================================================================================================  
    """)      
    

def execute_solve_problem_mode():
    """Execute the menu in 'Solve a problem' mode."""
    while True:
        reset_solve_problem_mode_interface()
        option = input(">> Introduce the number of the game mode you want to access: ")
        print()
        
        if option not in ["1", "2", "3"]:
            reset_solve_problem_mode_interface()
            print("Remember, only numbers from 1 to 3 are accepted. Please, try again.", end="\n\n")
            sleep(3)
            continue
            
        if option == "1":
            reset_solve_problem_mode_interface()
            print("You have selected the first option: Information about the mode.", end="\n\n")
            sleep(3)
            screen_reset()
            print_solve_problem_header()
            print_solve_problem_mode_info()
            input("Press any key to continue: ")
            continue
            
        elif option == "2":
            reset_solve_problem_mode_interface()
            print("You have selected the second option: Solve a problem.", end="\n\n")
            sleep(3)
            while True:
                print(">> Introduce the name of the problem you want to solve.", end="\n\n")
                file_name = input("Remember! Introduce the name of the problem without '.pickle' extension.")
                for item in pathlib.Path(".").iterdir():
                    if (file_name + ".pickle") == item.name and item.is_file():
                        solve_problem(file_name)
                else:
                    print()
                    print("The name introduced cannot be reproduced as a chess problem.", end="\n\n")
                    sleep(3)
                repeat = input("Do you want to try again? Select 'YES'/'NO': ")
                if repeat.upper() not in ["YES", "Y"]:
                    break
            
        elif option == "3":
            reset_solve_problem_mode_interface()
            print("You have selected the third option: Return to main menu.", end="\n\n")
            sleep(3)
            execute_main_menu()


if __name__ == "__main__":
    execute_main_menu()