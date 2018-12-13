import curses
import game
import ataxx

def borders(screen, game, x, y):
    screen.addstr(y   , x, "  a b c d e f g  ", curses.color_pair(3))
    screen.addstr(y+1 , x, " ╔═╦═╦═╦═╦═╦═╦═╗ ", curses.color_pair(3))

    for i in range(game.board.h):
        screen.addstr(y+2+2*i, x, F"{game.board.h-i}║ ║ ║ ║ ║ ║ ║ ║{game.board.h-i}", curses.color_pair(3))
        if i < game.board.h-1:
            screen.addstr(y+3+2*i, x, " ╠═╬═╬═╬═╬═╬═╬═╣ ", curses.color_pair(3))

    screen.addstr(y+15, x, " ╚═╩═╩═╩═╩═╩═╩═╝ ", curses.color_pair(3))
    screen.addstr(y+16, x, "  a b c d e f g  ", curses.color_pair(3))

def players(screen, game, x, y):
    # Player 1 --  details
    screen.addstr(y+14, x+20, F"{game.player1:<12}", curses.color_pair(3))
    screen.addstr(y+15, x+20, "Black       ", curses.color_pair(3))

    # Player 2 --  details
    screen.addstr(y+1, x+20,  "White       ", curses.color_pair(3))
    screen.addstr(y+2, x+20,  F"{game.player2:<12}", curses.color_pair(3))

def pieces(screen, game, x, y):
    for i in range(0, game.board.w):
        for j in range(0, game.board.h):
            piece = game.board.get(i, game.board.h-j-1)
            xcoord = x + 2*i + 2
            ycoord = y + 2*j + 2

            if piece == ataxx.BLACK:
                screen.addstr(ycoord, xcoord, "◉", curses.color_pair(3))
            elif piece == ataxx.WHITE:
                screen.addstr(ycoord, xcoord, "◉", curses.color_pair(4))
            elif piece == ataxx.GAP:
                screen.addstr(ycoord, xcoord, " ")
            elif piece == ataxx.EMPTY:
                screen.addstr(ycoord, xcoord, " ", curses.color_pair(4))

def timers(screen, game, x, y):
    if game.btime == None or game.wtime == None:
        screen.addstr(y+13, x+20, "--:--", curses.color_pair(3))
        screen.addstr(y+3, x+20, "--:--", curses.color_pair(3))
        return

    # Convert from ms to s and don't display negative times
    btime = max(game.btime//1000, 0)
    wtime = max(game.wtime//1000, 0)

    # Black
    bminutes = int(btime//60)
    bseconds = int(btime - 60*bminutes)
    bstr = F"{bminutes}:{bseconds:02d}"
    if len(bstr) < 12:
        bstr = bstr + " "*(12 - len(bstr))
    screen.addstr(y+13, x+20, bstr, curses.color_pair(3))

    # White
    wminutes = int(wtime//60)
    wseconds = int(wtime - 60*wminutes)
    wstr = F"{wminutes}:{wseconds:02d}"
    if len(wstr) < 12:
        wstr = wstr + " "*(12 - len(wstr))
    screen.addstr(y+3, x+20, wstr, curses.color_pair(3))

def status(screen, game, x, y):
    # Score
    black, white, gap, empty = game.board.count()
    screen.addstr(y+7, x+20, F" {black:>3} vs {white:<3} ", curses.color_pair(3))

    if game.board.turn == ataxx.BLACK:
        screen.addstr(y+8, x+20, "Black's turn", curses.color_pair(3))
    elif game.board.turn == ataxx.WHITE:
        screen.addstr(y+8, x+20, "White's turn", curses.color_pair(3))

def thinking(screen, game, x, y, n):
    if n:
        screen.addstr(y+9, x+20, "Thinking... ", curses.color_pair(3))
    else:
        screen.addstr(y+9, x+20, "            ")

def move(screen, game, x, y, input_str, turn, tick):
    if tick:
        char = "◉"
    else:
        char = " "

    screen.addstr(y+18, 2, F"Move:   {input_str[:4]:<4}", curses.color_pair(3))

    if turn:
        screen.addstr(y+18, 14, char, curses.color_pair(3))
    else:
        screen.addstr(y+18, 14, char, curses.color_pair(4))

def movelist(screen, game, x, y):
    height = 16
    yspace = 9
    for idx, move in enumerate(game.board.legal_moves()):
        xpos = (idx//height) * yspace
        ypos = idx%height
        screen.addstr(ypos, xpos+34, F"{idx+1:<2} {move}", curses.color_pair(3))
