import ataxx
import time

class Game():
    def __init__(self, btime, wtime, binc, winc, fen=None):
        self.board = ataxx.Board(fen)
        self.player1 = "Player 1"
        self.player2 = "Player 2"
        self.black_turn = self.board.turn == ataxx.Board.BLACK
        self.btime = btime
        self.wtime = wtime
        self.binc = binc
        self.winc = winc
        self.btime_last = btime
        self.wtime_last = wtime
        self.updated = True
        self.turn_start = None

    def play(self, san):
        try:
            move = self.board.parse_san(san)
            if self.board.is_legal(move):
                # Update the time tracking
                self.update()

                # Add increment
                if self.black_turn and self.btime != None and self.board.halfmove_clock >= 2:
                    self.btime += self.binc
                elif not self.black_turn and self.wtime != None and self.board.halfmove_clock >= 2:
                    self.wtime += self.winc

                # Apply move
                self.board.makemove(move)
                self.black_turn = (self.board.turn == ataxx.Board.BLACK)

                # Update time stores
                self.btime_last = self.btime
                self.wtime_last = self.wtime

                self.turn_start = time.time()

                self.updated = True
                return True
        except Exception as E:
            print(E)
            pass
        return False

    def update(self):
        if self.btime == None or self.wtime == None or self.board.gameover() or self.turn_start == None or self.board.halfmove_clock < 2:
            return

        turn_time = 1000*(time.time() - self.turn_start)

        if self.black_turn:
            self.btime = self.btime_last - turn_time
        else:
            self.wtime = self.wtime_last - turn_time
