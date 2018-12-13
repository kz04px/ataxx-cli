import curses
import draw
import random
import ataxx.uai
import queue
import threading
from game import *
from option import *

q = queue.Queue()

def show(settings):
    return curses.wrapper(game_window, settings)

def engine_think(engine, btime, wtime, binc, winc, difficulty=None):
    if difficulty == None:
        difficulty = "Easy"

    if difficulty == "Easy":
        bestmove, ponder = engine.go(movetime=20)
    elif difficulty == "Medium":
        bestmove, ponder = engine.go(movetime=100)
    elif difficulty == "Hard":
        bestmove, ponder = engine.go(movetime=1000)
    elif difficulty == "Extreme":
        if btime == None or wtime == None:
            bestmove, ponder = engine.go(movetime=2000)
        else:
            bestmove, ponder = engine.go(times=(btime, wtime, binc, winc))
    else:
        bestmove, ponder = engine.go(movetime=20)

    q.put(bestmove)

def game_window(stdscr, settings):
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    curses.curs_set(0)
    curses.halfdelay(5)

    # Settings -- position
    if settings["Board"].selected() == "default":
        fen = "startpos"
    elif settings["Board"].selected() == "4 corners":
        fen = "x5o/7/2-1-2/7/2-1-2/7/o5x x"
    else:
        fen = "startpos"

    # Settings -- time
    if settings["Time"].selected() == "1m+0s":
        btime, wtime, binc, winc = 60000, 60000, 0, 0
    elif settings["Time"].selected() == "3m+2s":
        btime, wtime, binc, winc = 180000, 180000, 2000, 2000
    elif settings["Time"].selected() == "10m+5s":
        btime, wtime, binc, winc = 600000, 600000, 5000, 5000
    elif settings["Time"].selected() == "None":
        btime, wtime, binc, winc = None, None, None, None

    game = Game(btime, wtime, binc, winc, fen=fen)

    # Settings -- player 1
    engine1 = None
    t1 = None
    if settings["Black"].selected() == "CPU":
        engine1 = ataxx.uai.Engine("./engines/tiktaxx")
        engine1.uai()
        engine1.isready()
        engine1.uainewgame()
        engine1.position(game.board)
        game.player1 = engine1.name

    # Settings -- player 2
    engine2 = None
    t2 = None
    if settings["White"].selected() == "CPU":
        engine2 = ataxx.uai.Engine("./engines/tiktaxx")
        engine2.uai()
        engine2.isready()
        engine2.uainewgame()
        engine2.position(game.board)
        game.player2 = engine2.name

    draw.borders(stdscr, game, 0, 0)
    draw.players(stdscr, game, 0, 0)
    draw.pieces(stdscr, game, 0, 0)
    draw.timers(stdscr, game, 0, 0)

    input_str = ""
    update_board = True
    thinking = False
    tick = True
    reason = None

    while True:
        tick = not tick
        game.update()

        # Draw things that update frequently
        draw.timers(stdscr, game, 0, 0)
        draw.thinking(stdscr, game, 0, 0, thinking)
        draw.move(stdscr, game, 0, 0, input_str, game.black_turn, tick)

        # Draw things that updat infrequently
        if update_board:
            draw.status(stdscr, game, 0, 0)
            draw.pieces(stdscr, game, 0, 0)
            draw.movelist(stdscr, game, 0, 0)
            update_board = False

            # Check if the game is over
            if game.board.gameover():
                result = game.board.result()
                if result == "1-0":
                    reason = "Black win"
                elif result == "0-1":
                    reason = "White win"
                elif result == "1/2-1/2":
                    reason = "Draw"
                break

        stdscr.move(18, 11)

        # Get input
        try:
            event = stdscr.getch()
        except KeyboardInterrupt:
            reason = "Resign"
            break
        except Exception as E:
            reason = "Error"
            break

        # Always handle these inputs
        if event == 27: # ESC
            break
        elif event == 127: # Backspace
            if len(input_str) > 0:
                input_str = input_str[:-1]

        san = None

        # Look for an engine move
        if not q.empty():
            san = q.get()
            q.task_done()

        if not thinking:
            if game.black_turn:
                if settings["Black"].selected() == "CPU":
                    engine1.position(game.board)
                    t1 = threading.Thread(
                        target=engine_think,
                        args=(
                            engine1,
                            game.btime,
                            game.wtime,
                            game.binc,
                            game.winc,
                            settings["Difficulty"].selected()
                        )
                    )
                    t1.daemon = True
                    t1.start()
                    thinking = True
                elif settings["Black"].selected() == "Human":
                    if event in [ord(n) for n in "abcdefgABCDEFG1234567"]:
                        input_str += chr(event)
                    elif event == ord("\n"):
                        san = input_str
                        input_str = ""
                else:
                    assert False
            else:
                if settings["White"].selected() == "CPU":
                    engine2.position(game.board)
                    t2 = threading.Thread(
                        target=engine_think,
                        args=(
                            engine2,
                            game.btime,
                            game.wtime,
                            game.binc,
                            game.winc,
                            settings["Difficulty"].selected()
                        )
                    )
                    t2.daemon = True
                    t2.start()
                    thinking = True
                elif settings["White"].selected() == "Human":
                    if event in [ord(n) for n in "abcdefgABCDEFG1234567"]:
                        input_str += chr(event)
                    elif event == ord("\n"):
                        san = input_str
                        input_str = ""
                else:
                    assert False

        # The engine might return a null move
        if san == "0000":
            reason = "nullmove"
            break
        # Try play a move if we have one
        elif san:
            r = game.play(san)
            if r:
                stdscr.addstr(18, 20, "             ")
                update_board = True
                thinking = False
            else:
                stdscr.addstr(18, 20, F"Illegal: {str(san):<4}", curses.color_pair(5))

                if game.black_turn and settings["Black"].selected() == "CPU":
                    reason = "Illegal engine move"
                    break
                if not game.black_turn and settings["White"].selected() == "CPU":
                    reason = "Illegal engine move"
                    break
            san = None

        # Check time left
        if game.btime != None and game.btime <= 0:
            reason = "Black loses on time"
            break
        if game.wtime != None and game.wtime <= 0:
            reason = "White loses on time"
            break

    # Stop the engines
    if engine1:
        engine1.quit()
    if engine2:
        engine2.quit()

    # Stop the engine threads
    if t1 and t1.is_alive():
        t1.join()
    if t2 and t2.is_alive():
        t2.join()

    curses.nocbreak()
    stdscr.addstr(8, 20, "Game over   ", curses.color_pair(3))
    stdscr.addstr(17, 20, F"{reason:<15}", curses.color_pair(5))
    stdscr.addstr(18, 20, "Play again? y/n", curses.color_pair(5))

    try:
        event = stdscr.getch()
    except:
        return False

    curses.flushinp()

    return event in [ord(n) for n in "yY"]
