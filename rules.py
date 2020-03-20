"""Rules module.

This module develops the rules needed to take a chess game.

The module includes:

    - Functions that describe the geometry of the board and the pieces' 
      movements.
    - Rules that imply move's restrictions, including the most important 
      rules in chess (check, checkmate and stalemate).
    - Classes for each pieces, which include pieces attributes (as color or 
      position) and some methods associated to their particular possibilities 
      in the game (movements or capture for example).

Rules module is the first part of 'Chess Masters's application and the core 
of its first game mode 'Play a game', which gives the possibility of taking 
a chess game.

"""



##### CONSTANTS #####

"""
The constant 'COLS' represents the name of the columns in board, while 'ROWS' 
represents rows' name.

The constant 'pieces' is not a constant at all but one of the most important 
variables in game. It represents the board as a list that includes the 
instances of all pieces in an specific position.

"""

COLS = "abcdefgh"
ROWS = "12345678"
pieces = []



##### FUNCTIONS #####

def increase(counter, n=1):
    """Increase a given counter by an amount of 'n'."""
    counter += n
    return counter


def seek_piece(position):
    """Return the instance of the piece in a given position."""
    for piece in pieces:
        if piece.position == position:
            return piece


def get_right_columns(column):
    """Return the columns on the right of a given column."""
    i = 0
    if column == "h":
        return None
    for i_column in COLS:
        if column == i_column:
            return COLS[i+1:]
        i = increase(i)

        
def get_left_columns(column):
    """Return the columns on the left of a given column."""
    i = 0
    if column == "a":
        return None
    for i_column in COLS:
        if column == i_column:
            return COLS[i-1::-1]
        i = increase(i)


def get_upper_rows(row):
    """Return the rows above a given row."""
    i = 0
    if row == "8":
        return None
    for i_row in ROWS:
        if row == i_row:
            return ROWS[i+1:]
        i = increase(i)

        
def get_lower_rows(row):
    """Return the rows below a given row."""
    i = 0
    if row == "1":
        return None
    for i_row in ROWS:
        if row == i_row:
            return ROWS[i-1::-1]
        i = increase(i)


def get_radjacent_col(column):
    """Return the right adjacent column of a given column."""
    return get_right_columns(column)[0] if column != "h" else None


def get_ladjacent_col(column):
    """Return the left adjacent column of a given column."""
    return get_left_columns(column)[0] if column != "a" else None


def get_upadjacent_row(row):
    """Return the row above a given row."""
    return get_upper_rows(row)[0] if row != "8" else None


def get_loadjacent_row(row):
    """Return the row below a given row."""
    return get_lower_rows(row)[0] if row != "1" else None


def allowed_movements(color):
    """Return a list with the allowed moves in a position for the side of a given color."""
    allowed_movements = []
    for piece in pieces:
        if piece.color == color:
            for move in piece.allow_movements():
                allowed_movements.append((piece.name, piece.position, move))
    return allowed_movements


def check_allowed_movements(color):
    """Return a list with the allowed movements in a check position for the side of a given color."""
    movements = []
    for (p_name, pos_1, pos_2) in allowed_movements(color):
        piece_1 = seek_piece(pos_1)
        piece_2 = seek_piece(pos_2)
        piece_1.set_position(pos_2)
        if piece_2:
            name = "X"
            name, piece_2.name = piece_2.name, name
        if not is_check(color):
            movements.append((p_name, pos_1, pos_2))
        piece_1.set_position(pos_1)
        if piece_2:
            piece_2.name = name
    return movements


def is_threatened(position, color):
    """Return 'True' if the given position is threatened by any piece of the other color. Otherwise return 'False'."""
    for piece in pieces:
        if piece.color != color:
            if piece.name == "R":
                if position in rook_movements(piece.position):
                    return True
            elif piece.name == "N":
                if position in knight_movements(piece.position):
                    return True
            elif piece.name == "B":
                if position in bishop_movements(piece.position):
                    return True
            elif piece.name == "Q":
                if position in queen_movements(piece.position):
                    return True
            elif piece.name == "K":
                if position in king_movements(piece.position):
                    return True
            elif piece.name == "P":
                if position in piece.pawn_capture_movements():
                    return True
    else:
        return False


def is_check(color):
    """Return 'True' if the King of a given color is in check. Otherwise return 'False'."""
    for piece in pieces:
        if piece.color == color and piece.name == "K":
            return is_threatened(piece.position, piece.color)


def is_checkmate(color):
    """Return 'True' if the King of a given color is in checkmate. Otherwise return 'False'."""
    condition1 = is_check(color)
    condition2 = not check_allowed_movements(color)
    return condition1 and condition2


def is_stalemate(color):
    """Return 'True' if the King of a given color is in stalemate. Otherwise return 'False'."""
    condition1 = not is_check(color)
    condition2 = not allowed_movements(color)
    return condition1 and condition2


def create(piece_name, color, position):
    """Create an instance of a piece, from a color in a determined position."""
    if piece_name == "R":
        pieces.append(Rook(color, position))
    elif piece_name == "N":
        pieces.append(Knight(color, position))
    elif piece_name == "B":
        pieces.append(Bishop(color, position))
    elif piece_name == "Q":
        pieces.append(Queen(color, position))
    elif piece_name == "K":
        pieces.append(King(color, position))
    elif piece_name == "P":
        pieces.append(Pawn(color, position))


def rook_movements(position):
    """Define the rook's movements in the board."""
    column, row = position[0], position[1]
    
    r_cols_moves = []
    if get_right_columns(column):
        for r_col in get_right_columns(column):
            r_cols_moves.append(r_col + row)
            if seek_piece(r_col + row):
                break
    
    l_cols_moves = []
    if get_left_columns(column):
        for l_col in get_left_columns(column):
            l_cols_moves.append(l_col + row)
            if seek_piece(l_col + row):
                break
        
    up_rows_moves = []
    if get_upper_rows(row):
        for up_row in get_upper_rows(row):
            up_rows_moves.append(column + up_row)
            if seek_piece(column + up_row):
                break
    
    lo_rows_moves = []
    if get_lower_rows(row):
        for lo_row in get_lower_rows(row):
            lo_rows_moves.append(column + lo_row)
            if seek_piece(column + lo_row):
                break
            
    movements = r_cols_moves + l_cols_moves + up_rows_moves + lo_rows_moves
    
    return movements


def knight_movements(position):
    """Define the knight's movements in the board."""
    column, row = position[0], position[1]
    
    upper_row_1 = get_upadjacent_row(row)
    upper_row_2 = get_upadjacent_row(upper_row_1) if upper_row_1 else None
    lower_row_1 = get_loadjacent_row(row)
    lower_row_2 = get_loadjacent_row(lower_row_1) if lower_row_1 else None
    right_col_1 = get_radjacent_col(column)
    right_col_2 = get_radjacent_col(right_col_1) if right_col_1 else None
    left_col_1 = get_ladjacent_col(column)
    left_col_2 = get_ladjacent_col(left_col_1) if left_col_1 else None
    
    upper_moves = []
    if upper_row_2 and right_col_1:
        upper_moves.append(right_col_1 + upper_row_2)
    if upper_row_1 and right_col_2:
        upper_moves.append(right_col_2 + upper_row_1)
    if upper_row_2 and left_col_1:
        upper_moves.append(left_col_1 + upper_row_2)
    if upper_row_1 and left_col_2:
        upper_moves.append(left_col_2 + upper_row_1)
        
    lower_moves =[]
    if lower_row_2 and right_col_1: 
        lower_moves.append(right_col_1 + lower_row_2)
    if lower_row_1 and right_col_2: 
        lower_moves.append(right_col_2 + lower_row_1) 
    if lower_row_2 and left_col_1: 
        lower_moves.append(left_col_1 + lower_row_2)
    if lower_row_1 and left_col_2:
        lower_moves.append(left_col_2 + lower_row_1)
    
    movements = upper_moves + lower_moves

    return movements


def bishop_movements(position):
    """Define the bishop's movements in the board."""
    column, row = position[0], position[1]
    
    r_upper_moves = []
    if get_right_columns(column) and get_upper_rows(row):
        for i_col, i_row in zip(get_right_columns(column), get_upper_rows(row)):
            r_upper_moves.append(i_col + i_row)
            if seek_piece(i_col + i_row):
                break
    
    l_upper_moves = []
    if get_left_columns(column) and get_upper_rows(row):
        for i_col, i_row in zip(get_left_columns(column), get_upper_rows(row)):
            l_upper_moves.append(i_col + i_row)
            if seek_piece(i_col + i_row):
                break
    
    r_lower_moves = []
    if get_right_columns(column) and get_lower_rows(row):    
        for i_col, i_row in zip(get_right_columns(column), get_lower_rows(row)):
            r_lower_moves.append(i_col + i_row)
            if seek_piece(i_col + i_row):
                break
    
    l_lower_moves = []
    if get_left_columns(column) and get_lower_rows(row):
        for i_col, i_row in zip(get_left_columns(column), get_lower_rows(row)):
            l_lower_moves.append(i_col + i_row)
            if seek_piece(i_col + i_row):
                break
        
    movements = r_upper_moves + l_upper_moves + r_lower_moves + l_lower_moves
    
    return movements


def queen_movements(position):
    """Define the queen's movements in the board."""
    return rook_movements(position) + bishop_movements(position)


def king_movements(position):
    """Define the king's movements in the board."""
    column, row = position[0], position[1]
    
    upper_row = get_upadjacent_row(row)
    lower_row = get_loadjacent_row(row)
    right_col = get_radjacent_col(column)
    left_col = get_ladjacent_col(column)
    
    upper_moves = []
    if upper_row:
        upper_moves.append(column + upper_row)
    if upper_row and right_col:
        upper_moves.append(right_col + upper_row)
    if upper_row and left_col:
        upper_moves.append(left_col + upper_row)
        
    row_moves = []
    if right_col:
        row_moves.append(right_col + row)
    if left_col:
        row_moves.append(left_col + row)
        
    lower_moves =[]
    if lower_row:
        lower_moves.append(column + lower_row)
    if lower_row and right_col:
        lower_moves.append(right_col + lower_row)
    if lower_row and left_col:
        lower_moves.append(left_col + lower_row)
    
    movements = upper_moves + row_moves + lower_moves
    
    return movements


def pawn_movements(color, position):
    """Define the pawn's movements in the board."""
    column, row = position[0], position[1]

    if color == "w":
        if row == "2":
            movements = [column + str(int(row)+1), column + str(int(row)+2)]
        elif row in "34567":
            movements = [column + str(int(row)+1)]
            
    elif color == "b":
        if row == "7":
            movements = [column + str(int(row)-1), column + str(int(row)-2)]
        elif row in "23456":
            movements = [column + str(int(row)-1)]
            
    return movements


##### CLASSES #####

class Piece:
    """The main class for chess pieces."""
    pass


class Rook(Piece):
    """Class for rook in chess."""
    def __init__(self, color, position):
        """Construction of a rook instance."""
        self.name = "R"
        self.color = color
        self.position = position
        self.column = position[0]
        self.row = position[1]
        self.castling = True
        
    def __repr__(self):
        """Representation of a rook instance."""
        return f"Rook('{self.color}', '{self.position}')"
        
    def is_correct(self):
        """Check that the position of the instance is correct according to chess rules."""
        row_correct = True if self.row in "12345678" else False
        col_correct = True if self.column in "abcdefgh" else False
        return all([row_correct, col_correct])
    
    def set_position(self, new_position):
        """Set the piece to a new position in the board."""
        self.position = new_position
        self.column = new_position[0]
        self.row = new_position[1]
        
    def allow_movements(self):
        """Return a list with the allowed movements for the piece in the board."""
        movements = rook_movements(self.position)
        for move in movements[:]:
            piece = seek_piece(move)
            if piece:
                if piece.color == self.color:
                    movements.remove(move)
        return movements
    
    def move(self, position):
        """Move the piece according to an allowed movement to a position."""
        if position in self.allow_movements():
            piece = seek_piece(position)
            if piece:
                print("A piece has been captured!", end="\n\n")
                pieces.remove(piece)
            self.position = position
            self.column = position[0]
            self.row = position[1]
            self.castling = False
        else:
            print("Invalid movement.", end="\n\n")


class Knight(Piece):
    """Class for knight in chess."""
    def __init__(self, color, position):
        """Construction of a knight instance."""
        self.name = "N"
        self.color = color
        self.position = position
        self.column = position[0]
        self.row = position[1]
        
    def __repr__(self):
        """Representation of a knight instance."""
        return f"Knight('{self.color}', '{self.position}')"
        
    def is_correct(self):
        """Check that the position of the instance is correct according to chess rules."""
        row_correct = True if self.row in "12345678" else False
        col_correct = True if self.column in "abcdefgh" else False
        return all([row_correct, col_correct])
    
    def set_position(self, new_position):
        """Set the piece to a new position in the board."""
        self.position = new_position
        self.column = new_position[0]
        self.row = new_position[1]
        
    def allow_movements(self): 
        """Return a list with the allowed movements for the piece in the board."""
        movements = knight_movements(self.position)
        for move in movements[:]:
            piece = seek_piece(move)
            if piece:
                if piece.color == self.color:
                    movements.remove(move)
        return movements
                
    def move(self, position):
        """Move the piece according to an allowed movement to a position."""
        if position in self.allow_movements():
            piece = seek_piece(position)
            if piece:
                print("A piece has been captured!", end="\n\n")
                pieces.remove(piece)
            self.position = position
            self.column = position[0]
            self.row = position[1]
        else:
            print("Invalid movement.", end="\n\n")


class Bishop(Piece):
    """Class for bishop in chess."""
    def __init__(self, color, position):
        """Construction of a bishop instance."""
        self.name = "B"
        self.color = color
        self.position = position
        self.column = position[0]
        self.row = position[1]
        
    def __repr__(self):
        """Representation of a bishop instance."""
        return f"Bishop('{self.color}', '{self.position}')"
        
    def is_correct(self):
        """Check that the position of the instance is correct according to chess rules."""
        row_correct = True if self.row in "12345678" else False
        col_correct = True if self.column in "abcdefgh" else False
        return all([row_correct, col_correct])
    
    def set_position(self, new_position):
        """Set the piece to a new position in the board."""
        self.position = new_position
        self.column = new_position[0]
        self.row = new_position[1]
        
    def allow_movements(self):   
        """Return a list with the allowed movements for the piece in the board."""
        movements = bishop_movements(self.position)
        for move in movements[:]:
            piece = seek_piece(move)
            if piece:
                if piece.color == self.color:
                    movements.remove(move)
        return movements
    
    def move(self, position):
        """Move the piece according to an allowed movement to a given position."""
        if position in self.allow_movements():
            piece = seek_piece(position)
            if piece:
                print("A piece has been captured!", end="\n\n")
                pieces.remove(piece)
            self.position = position
            self.column = position[0]
            self.row = position[1]
        else:
            print("Invalid movement.", end="\n\n")


class Queen(Piece):
    """Class for queen in chess."""
    def __init__(self, color, position):
        """Construction of a queen instance."""
        self.name = "Q"
        self.color = color
        self.position = position
        self.column = position[0]
        self.row = position[1]
        
    def __repr__(self):
        """Representation of a queen instance."""
        return f"Queen('{self.color}', '{self.position}')"
        
    def is_correct(self):
        """Check that the position of the instance is correct according to chess rules."""
        row_correct = True if self.row in "12345678" else False
        col_correct = True if self.column in "abcdefgh" else False
        return all([row_correct, col_correct])
    
    def set_position(self, new_position):
        """Set the piece to a new position in the board."""
        self.position = new_position
        self.column = new_position[0]
        self.row = new_position[1]
        
    def allow_movements(self):      
        """Return a list with the allowed movements for the piece in the board."""
        movements = queen_movements(self.position)
        for move in movements[:]:
            piece = seek_piece(move)
            if piece:
                if piece.color == self.color:
                    movements.remove(move)
        return movements
    
    def move(self, position):
        """Move the piece according to an allowed movement to a given position."""
        if position in self.allow_movements():
            piece = seek_piece(position)
            if piece:
                print("A piece has been captured!", end="\n\n")
                pieces.remove(piece)
            self.position = position
            self.column = position[0]
            self.row = position[1]
        else:
            print("Invalid movement.", end="\n\n")


class King(Piece):
    """Class for king in chess."""
    def __init__(self, color, position):
        """Construction of a king instance."""
        self.name = "K"
        self.color = color
        self.position = position
        self.column = position[0]
        self.row = position[1]
        self.castling = True
        
    def __repr__(self):
        """Representation of a king instance."""
        return f"King('{self.color}', '{self.position}')"
        
    def is_correct(self):
        """Check that the position of the instance is correct according to chess rules."""
        row_correct = True if self.row in "12345678" else False
        col_correct = True if self.column in "abcdefgh" else False
        return all([row_correct, col_correct])
    
    def set_position(self, new_position):
        """Set the piece to a new position in the board."""
        self.position = new_position
        self.column = new_position[0]
        self.row = new_position[1]
        
    def allow_movements(self):       
        """Return a list with the allowed movements for the piece in the board."""
        movements = king_movements(self.position)
        for move in movements[:]:
            piece = seek_piece(move)
            if piece:
                if piece.color == self.color:
                    movements.remove(move)
        for move in movements[:]:
            if is_threatened(move, self.color):
                movements.remove(move)             
        return movements
    
    def move(self, position):
        """Move the piece according to an allowed movement to a given position."""
        if position in self.allow_movements():
            piece = seek_piece(position)
            if piece:
                print("A piece has been captured!", end="\n\n")
                pieces.remove(piece)
            self.position = position
            self.column = position[0]
            self.row = position[1]
            self.castling = False
            
        elif position == "0-0":
            if self.castling_move("kingside"):
                self.castling = False
                self.column = "g"
                self.row = "1" if self.color == "w" else "8"
                self.position = "g1" if self.color == "w" else "g8"
                rook_pos = "h1" if self.color == "w" else "h8"
                seek_piece(rook_pos).column = "f"
                seek_piece(rook_pos).row = "1" if self.color == "w" else "8"
                seek_piece(rook_pos).position = "f1" if self.color == "w" else "f8"
            else:
                print("Invalid castling movement.", end="\n\n")
                
        elif position == "0-0-0":
            if self.castling_move("queenside"):
                self.castling = False
                self.column = "c"
                self.row = "1" if self.color == "w" else "8"
                self.position = "c1" if self.color == "w" else "c8"
                rook_pos = "a1" if self.color == "w" else "a8" 
                seek_piece(rook_pos).column = "d"
                seek_piece(rook_pos).row = "1" if self.color == "w" else "8"
                seek_piece(rook_pos).position = "d1" if self.color == "w" else "d8"
            else:
                print("Invalid castling movement.", end="\n\n")
        
        else:
            print("Invalid movement.", end="\n\n")

    def castling_move(self, castle):
        """Execute king's castling movement."""
        if self.color == "w":
            if castle == "kingside":
                piece = seek_piece("h1")
                if not piece:
                    return False
                else:
                    if seek_piece("h1").name != "R" or self.position != "e1":
                        return False
                cond1 = [self.castling and seek_piece("h1").castling]
                cond2 = [not seek_piece("f1"), not seek_piece("g1")]
                cond3 = [not is_threatened("e1", "w"), 
                         not is_threatened("f1", "w"), 
                         not is_threatened("g1", "w")]

                return all(cond1 + cond2 + cond3)
            
            elif castle == "queenside":
                piece = seek_piece("a1")
                if not piece:
                    return False
                else:
                    if seek_piece("a1").name != "R" or self.position != "e1":
                        return False
                cond1 = [self.castling and seek_piece("a1").castling]
                cond2 = [not seek_piece("d1"), 
                         not seek_piece("c1"), 
                         not seek_piece("b1")]
                cond3 = [not is_threatened("e1", "w"), 
                         not is_threatened("d1", "w"), 
                         not is_threatened("c1", "w")]

                return all(cond1 + cond2 + cond3)
                
        if self.color == "b":
            if castle == "kingside":
                piece = seek_piece("h8")
                if not piece:
                    return False
                else:
                    if seek_piece("h8").name != "R" or self.position != "e8":
                        return False
                cond1 = [self.castling and seek_piece("h8").castling]
                cond2 = [not seek_piece("f8"), not seek_piece("g8")]
                cond3 = [not is_threatened("e8", "b"), 
                         not is_threatened("f8", "b"), 
                         not is_threatened("g8", "b")]

                return all(cond1 + cond2 + cond3)        
                
            elif castle == "queenside":
                piece = seek_piece("a8")
                if not piece:
                    return False
                else:
                    if seek_piece("a8").name != "R" or self.position != "e8":
                        return False
                cond1 = [self.castling and seek_piece("a8").castling]
                cond2 = [not seek_piece("d8"), 
                         not seek_piece("c8"), 
                         not seek_piece("b8")]
                cond3 = [not is_threatened("e8", "b"), 
                         not is_threatened("d8", "b"), 
                         not is_threatened("c8", "b")]
                         
                return all(cond1 + cond2 + cond3)


class Pawn(Piece):
    """Class for pawn in chess."""
    def __init__(self, color, position):
        """Construction of a pawn instance."""
        self.name = "P"
        self.color = color
        self.position = position
        self.column = position[0]
        self.row = position[1]
        
    def __repr__(self):
        """Representation of a pawn instance."""
        return f"Pawn('{self.color}', '{self.position}')"
        
    def is_correct(self):
        """Check that the position of the instance is correct according to chess rules."""
        row_correct = True if self.row in "234567" else False
        col_correct = True if self.column in "abcdefgh" else False
        return all([row_correct, col_correct])
    
    def set_position(self, new_position):
        """Sets the piece to a new position in the board."""
        self.position = new_position
        self.column = new_position[0]
        self.row = new_position[1]
        
    def pawn_capture_movements(self):
        """Return a list with a pawn capture movements allowed."""
        capture_movements = []
        
        if self.color == "w":
            r_col = get_radjacent_col(self.column)
            l_col = get_ladjacent_col(self.column) 
            up_row = get_upadjacent_row(self.row)
            if r_col and up_row:
                capture_movements.append(r_col + up_row) 
            if l_col and up_row:
                capture_movements.append(l_col + up_row)    
            return capture_movements
            
        elif self.color == "b":
            r_col = get_radjacent_col(self.column)
            l_col = get_ladjacent_col(self.column) 
            lo_row = get_loadjacent_row(self.row)
            if r_col and lo_row:
                capture_movements.append(r_col + lo_row)    
            if l_col and lo_row:
                capture_movements.append(l_col + lo_row)
            return capture_movements
    
    def allow_movements(self):
        """Return a list with the allowed movements for the piece in the board."""
        movements = pawn_movements(self.color, self.position)
        for move in movements[:]:
            piece = seek_piece(move)
            if piece:
                movements.remove(move)
        if self.row == "2":
            piece = seek_piece(self.column + get_upadjacent_row(self.row))
            if piece:
                movements = []
        if self.row == "7":
            piece = seek_piece(self.column + get_loadjacent_row(self.row))
            if piece:
                movements = []
        capture_movements = self.pawn_capture_movements()
        for move in capture_movements[:]:
            piece = seek_piece(move)
            if not piece or piece.color == self.color:
                capture_movements.remove(move)
            
        return movements + capture_movements

    def move(self, position):
        """Move the piece according to an allowed movement to a given position."""
        if position in self.allow_movements():
            piece = seek_piece(position)
            if piece:
                print("A piece has been captured!", end="\n\n")
                pieces.remove(piece)
            self.position = position
            self.column = position[0]
            self.row = position[1]
            if self.color == "w":
                if self.row == "8":
                    self.promote()
            elif self.color == "b":
                if self.row == "1":
                    self.promote()
        else:
            print("Invalid movement.", end="\n\n")
            
    def promote(self):
        """Promote a pawn."""
        print("Promoting pawn.", end="\n\n")
        pieces.remove(self)
        repeat = True
        while repeat:
            piece = input(">> Introduce the piece you want to promote to (R, N, B, Q): ")
            piece = piece.upper()
            if piece == "":
                repeat = False
                create("Q", self.color, self.position)
            elif piece in "RNBQ":
                repeat = False
                if piece == "R":
                    create("R", self.color, self.position)
                elif piece == "N":
                    create("N", self.color, self.position)
                elif piece == "B":
                    create("B", self.color, self.position)
                elif piece == "Q":
                    create("Q", self.color, self.position)
            else:
                print("Please, introduce a valid name.", end="\n\n")