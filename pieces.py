import chess, ai

class Piece(object):

    WHITE = "W"
    BLACK = "B"

    def __init__(self, x, y, color, piece_type):
        self.x = x
        self.y = y
        self.color = color
        self.piece_type = piece_type

    # Returns all diagonal moves for this piece. This should therefore only
    # be used by the Bishop and Queen since they are the only pieces that can
    # move diagonally.
    def get_possible_diagonal_moves(self, board):
        moves = []

        for i in range(1, chess.Board.WIDTH):
            if (not board.in_bounds(self.x+i, self.y+i)):
                break

            piece = board.get_piece(self.x+i, self.y+i)
            moves.append(self.get_move(board, self.x+i, self.y+i))
            if (piece != 0):
                break

        for i in range(1, chess.Board.WIDTH):
            if (not board.in_bounds(self.x+i, self.y-i)):
                break

            piece = board.get_piece(self.x+i, self.y-i)
            moves.append(self.get_move(board, self.x+i, self.y-i))
            if (piece != 0):
                break

        for i in range(1, chess.Board.WIDTH):
            if (not board.in_bounds(self.x-i, self.y-i)):
                break

            piece = board.get_piece(self.x-i, self.y-i)
            moves.append(self.get_move(board, self.x-i, self.y-i))
            if (piece != 0):
                break

        for i in range(1, chess.Board.WIDTH):
            if (not board.in_bounds(self.x-i, self.y+i)):
                break

            piece = board.get_piece(self.x-i, self.y+i)
            moves.append(self.get_move(board, self.x-i, self.y+i))
            if (piece != 0):
                break

        return self.remove_null_from_list(moves)

    # Returns all horizontal moves for this piece. This should therefore only
    # be used by the Rooks and Queen since they are the only pieces that can
    # move horizontally.
    def get_possible_horizontal_moves(self, board):
        moves = []

        # Moves to the right of the piece.
        for i in range(1, chess.Board.WIDTH - self.x):
            piece = board.get_piece(self.x + i, self.y)
            moves.append(self.get_move(board, self.x+i, self.y))

            if (piece != 0):
                break

        # Moves to the left of the piece.
        for i in range(1, self.x + 1):
            piece = board.get_piece(self.x - i, self.y)
            moves.append(self.get_move(board, self.x-i, self.y))
            if (piece != 0):
                break

        # Downward moves.
        for i in range(1, chess.Board.HEIGHT - self.y):
            piece = board.get_piece(self.x, self.y + i)
            moves.append(self.get_move(board, self.x, self.y+i))
            if (piece != 0):
                break

        # Upward moves.
        for i in range(1, self.y + 1):
            piece = board.get_piece(self.x, self.y - i)
            moves.append(self.get_move(board, self.x, self.y-i))
            if (piece != 0):
                break

        return self.remove_null_from_list(moves)

    # Returns a Move object with (xfrom, yfrom) set to the piece current position.
    # (xto, yto) is set to the given position. If the move is not valid 0 is returned.
    # A move is not valid if it is out of bounds, or a piece of the same color is
    # being eaten.
    def get_move(self, board, xto, yto):
        move = 0
        if (board.in_bounds(xto, yto)):
            piece = board.get_piece(xto, yto)
            if (piece != 0):
                if (piece.color != self.color):
                    move = ai.Move(self.x, self.y, xto, yto)
            else:
                move = ai.Move(self.x, self.y, xto, yto)
        return move

    # Returns the list of moves cleared of all the 0's.
    def remove_null_from_list(self, l):
        return [move for move in l if move != 0]

    def to_string(self):
        return self.color + self.piece_type + " "

class Rook(Piece):

    PIECE_TYPE = "R"

    def __init__(self, x, y, color):
        super(Rook, self).__init__(x, y, color, Rook.PIECE_TYPE)

    def get_possible_moves(self, board):
        return self.get_possible_horizontal_moves(board)


class Knight(Piece):

    PIECE_TYPE = "N"

    def __init__(self, x, y, color):
        super(Knight, self).__init__(x, y, color, Knight.PIECE_TYPE)

    def get_possible_moves(self, board):
        moves = []

        moves.append(self.get_move(board, self.x+2, self.y+1))
        moves.append(self.get_move(board, self.x-1, self.y+2))
        moves.append(self.get_move(board, self.x-2, self.y+1))
        moves.append(self.get_move(board, self.x+1, self.y-2))
        moves.append(self.get_move(board, self.x+2, self.y-1))
        moves.append(self.get_move(board, self.x+1, self.y+2))
        moves.append(self.get_move(board, self.x-2, self.y+1))
        moves.append(self.get_move(board, self.x-1, self.y-2))

        return self.remove_null_from_list(moves)


class Bishop(Piece):

    PIECE_TYPE = "B"

    def __init__(self, x, y, color):
        super(Bishop, self).__init__(x, y, color, Bishop.PIECE_TYPE)

    def get_possible_moves(self, board):
        return self.get_possible_diagonal_moves(board)


class Queen(Piece):

    PIECE_TYPE = "Q"

    def __init__(self, x, y, color):
        super(Queen, self).__init__(x, y, color, Queen.PIECE_TYPE)

    def get_possible_moves(self, board):
        diagonal = self.get_possible_diagonal_moves(board)
        horizontal = self.get_possible_horizontal_moves(board)
        return diagonal + horizontal

class King(Piece):

    PIECE_TYPE = "K"

    def __init__(self, x, y, color):
        super(King, self).__init__(x, y, color, King.PIECE_TYPE)

    def get_possible_moves(self, board):
        moves = []

        moves.append(self.get_move(board, self.x+1, self.y))
        moves.append(self.get_move(board, self.x+1, self.y+1))
        moves.append(self.get_move(board, self.x, self.y+1))
        moves.append(self.get_move(board, self.x-1, self.y+1))
        moves.append(self.get_move(board, self.x-1, self.y))
        moves.append(self.get_move(board, self.x-1, self.y-1))
        moves.append(self.get_move(board, self.x, self.y-1))
        moves.append(self.get_move(board, self.x+1, self.y-1))

        return self.remove_null_from_list(moves)

class Pawn(Piece):

    PIECE_TYPE = "P"

    def __init__(self, x, y, color):
        super(Pawn, self).__init__(x, y, color, Pawn.PIECE_TYPE)

    def is_starting_position(self):
        if (self.color == Piece.BLACK):
            return self.x == board.Board.WIDTH - 2
        else:
            return self.x == 1

    def get_possible_moves(self, board):
        moves = []

        # Direction the pawn can move in.
        direction = 1
        if (self.color == Piece.BLACK):
            direction = -1

        # The general 1 step forward move.
        moves.append(self.get_move(board, self.x + direction, self.y))

        # The Pawn can take 2 steps as the first move.
        if (self.is_starting_position() and board.get_piece(self.x + direction, self.y) == 0):
            moves.append(self.get_move(board, self.x + direction * 2, self.y))

        # Eating pieces.
        piece = board.get_piece(self.x + direction, self.y + 1)
        if (piece != 0):
            moves.append(self.get_move(board, self.x + direction, self.y + 1))

        piece = board.get_piece(self.x + direction, self.y - 1)
        if (piece != 0):
            moves.append(self.get_move(board, self.x + direction, self.y - 1))

        return self.remove_null_from_list(moves)