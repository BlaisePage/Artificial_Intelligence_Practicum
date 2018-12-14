'''

Practicum: Python Chess AI
Authors: Blaise Page and Phillip (Armen) Arsenian
CSCI 3202: Intro to Artificial Intelligence
Professor: Chris Heckman


'''

'''
In order to run this program you must first install python-chess.
To install python-chess run the command:
    pip3 install python-chess

Once python-chess is installed, run the following command in this file's directory:
    python3 minimax_chess_AI.py

Then play the game!

Also note, that I play with with a dark terminal, for this reason I have inverted the colors of the chess pieces. It is recommended to use a terminal with a non black/white background
'''

'''
depth=1:
depth=2: 1:26
depth=3:
'''

'''
Variation of 4s maneuver that "might" win with depth 2:
As White, play: 8,12,18,38,10 => Note, move numbers may differ slightly
As Black, play:
'''

import chess
import random
import sys
import collections
from time import sleep
import timeit
import numpy as np

''' AI Minimax Agent '''
class AlphaBetaAgent:
    """
      Your minimax agent with alpha-beta pruning
    """

    def __init__(self, board):
        self.depth = 2 # set the depth
        self.finished = 0 # bool to determine when the game is over

    ''' Change the eval function to match the scoring system '''
    def evaluationFunction(self, board):

        '''
        Scoring System:

        A pawn is worth 1
        A knight is worth 3
        A bishop is worth 3
        A rook is worth 5
        A queen is worth 9
        The king is infinitely valuable
        '''

        board_copy = board.copy()
        black_dict = {}
        white_dict = {}
        squares = chess.SQUARES
        for i in range(0,len(squares)):
            #print(squares[i])
            piece = board_copy.remove_piece_at(squares[i])
            piece_string = str(piece)

            if(piece_string.isupper()):

                if(piece_string not in white_dict):
                    white_dict[piece_string] = 1
                else:
                    white_dict[piece_string] += 1

            if(piece_string.islower()):

                if(piece_string not in black_dict):
                    black_dict[piece_string] = 1
                else:
                    black_dict[piece_string] += 1

        white_count = 0
        black_count = 0

        # calculate the score for white
        for white_piece in white_dict:

            if(white_piece == "P"):
                white_count += white_dict[white_piece]
            elif(white_piece == "N"):
                white_count += white_dict[white_piece]*3
            elif(white_piece == "B"):
                white_count += white_dict[white_piece]*3
            elif(white_piece == "R"):
                white_count += white_dict[white_piece]*5
            elif(white_piece == "Q"):
                white_count += white_dict[white_piece]*9
            elif(white_piece == "K"):
                white_count += white_dict[white_piece]*1000

        # calculate the score for black
        for black_piece in black_dict:

            if(black_piece == "p"):
                black_count += black_dict[black_piece]
            elif(black_piece == "n"):
                black_count += black_dict[black_piece]*3
            elif(black_piece == "b"):
                black_count += black_dict[black_piece]*3
            elif(black_piece == "r"):
                black_count += black_dict[black_piece]*5
            elif(black_piece == "q"):
                black_count += black_dict[black_piece]*9
            elif(black_piece == "k"):
                black_count += black_dict[black_piece]*1000

        # Avoid white check
        if((board.turn) and (board.is_check())):
            white_count -= 10
        # Avoid black check
        if((not board.turn) and (board.is_check())):
            black_count -= 10

        # Avoid white checkmate
        if((board.turn) and (board.is_checkmate())):
            white_count -= 1000
        # Avoid black checkmate
        if((not board.turn) and (board.is_checkmate())):
            black_count -= 1000

        # White's move
        if(board.turn):
            return (white_count - black_count)
        # Black's move
        else:
            return (black_count - white_count)




    def getAction(self, board):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float("-inf")
        beta = float("inf")
        return self.alphabeta_search(board, 0, 0, alpha, beta)

    def successorBoard(self, board, move):

        successor_board = board.copy()
        curr_move = chess.Move.from_uci(move)
        successor_board.push(curr_move)
        return successor_board


    def alphabeta_search(self, board, agent_number, curr_depth, alpha, beta):

        #print("test1")

        #print(curr_depth)
        #print(agent_number)
        #return immediately if it is a terminal state
        if(board.is_game_over()):

            # check the following return ?????
            return float("inf")

        # check to see if all agents have been covered
        # White = 0, Black = 1
        if(agent_number > 1):
            agent_number = 0
            curr_depth = curr_depth+1

        # if we have reached the max depth we are at a terminal state
        if(curr_depth == self.depth):
            return self.evaluationFunction(board)

        # call max_value iff agent is pacman else call min_value
        if(agent_number == 0):
            return self.max_value(board, agent_number, curr_depth, alpha, beta)
        else:
            return self.min_value(board, agent_number, curr_depth, alpha, beta)


    def min_value(self, board, agent_number, curr_depth, alpha, beta):

        best_value = float("inf")
        best_action = None

        # Get a list of possible moves
        move_list = []
        possible_moves = board.legal_moves
        #print(possible_moves)
        for i in possible_moves:
            move_list.append(str(i))

        # iterate over moves and save the min value
        for move in move_list:

            next_state = self.successorBoard(board, move)
            value = best_value
            value = self.alphabeta_search(next_state, agent_number+1, curr_depth, alpha, beta)
            #print(value)
            if(value < best_value):
                best_value = value
                best_action = move

            if(best_value < alpha):
                return best_value
            beta = min(best_value, beta)

        return best_value


    def max_value(self, board, agent_number, curr_depth, alpha, beta):

        best_value = float("-inf")

        # Get a list of possible moves
        move_list = []
        possible_moves = board.legal_moves
        #print(possible_moves)
        for i in possible_moves:
            move_list.append(str(i))


        # iterate over all pacman actions pacman actions and save the max value and its corresponding action
        for move in move_list:
            # find the action that result in the highest score
            next_state = self.successorBoard(board, move)
            value = self.alphabeta_search(next_state, agent_number+1, curr_depth, alpha, beta)
            if(value > best_value):
                best_value = value
                best_action = move
            if(best_value > beta):
                return best_value
            alpha = max(best_value, alpha)

        # return the optimal action iff the depth is 0
        if(curr_depth == 0):
            return best_action
        else:
            return best_value


''' Main Menu '''
def main():

    print("")
    print("")
    print("--------- Welcome To Terminal Chess ---------")
    print("")

    option = "-1"

    while(option != "3"):

        # Menu
        print("")
        print("Select a game mode:")
        print("")
        print("1. AI vs AI")
        print("2. Player vs AI (recommended option)")
        print("3. Quit")
        print("")
        option = str(input())

        # AI vs AI
        if(option == "1"):

            print("Minimax vs Minimax")

            board = chess.Board()
            agent = AlphaBetaAgent(board)

            mean_time = []

            ''' Start the Game '''
            while(not board.is_game_over()):

                # Display the board in the terminal
                print("")
                print(board.unicode(invert_color = True, borders = True)) #change these values to alter the way that the board prints
                print("")
                print("The minimax agent is making a move... This could take a while...")
                # get the best action
                #start = timeit.timeit()
                action = agent.getAction(board)
                #end = timeit.timeit()
                #time = (end-start)
                #print(time)
                #mean_time.append(time)

                #print(action)
                # make the move
                curr_move = chess.Move.from_uci(action)
                #print(curr_move)
                board.push(curr_move)


                # sleep to slow down moves
                #sleep(1)

            turn = board.turn
            if(not turn):
                print("White Wins!")
            else:
                print("Black Wins!")

            board.clear()

            print("Average AI move time: ", np.mean(mean_time))

        # Player vs AI
        elif(option == "2"):

            print("Minimax vs Player")
            print("")
            print("Pick Side:")
            print("")
            print("1. White")
            print("2. Black")
            side = input()

            board = chess.Board()
            agent = AlphaBetaAgent(board)

            mean_time = []

            while((not board.is_game_over() and ((side=="1")or(side=="2")))):

                # Display the board in the terminal
                print("")
                print(board.unicode(invert_color = True, borders = True)) #change these values to alter the way that the board prints
                print("")

                # player chose white
                if(side == "1"):

                    # player's turn
                    if(board.turn):

                        # get possible moves and put them in a dict for choosing
                        possible_moves = board.legal_moves
                        move_dict = collections.OrderedDict()
                        #print(possible_moves)
                        move_count = 1
                        for move in possible_moves:
                            move_count_string = str(move_count)
                            move_dict[move_count_string] = str(move)
                            move_count += 1

                        # have the player select a move
                        print(move_dict)
                        print("Select a move from above:")
                        player_move = input()

                        # make the move
                        action = move_dict[player_move]
                        curr_move = chess.Move.from_uci(action)
                        #print(curr_move)
                        board.push(curr_move)

                    # AI's turn
                    else:

                        print("The minimax agent is making a move... This could take a while...")

                        #start = timeit.timeit()
                        action = agent.getAction(board)
                        #end = timeit.timeit()
                        #time = (end-start)
                        #print(time)
                        #mean_time.append(time)

                        #print(action)
                        # make the move
                        curr_move = chess.Move.from_uci(action)
                        #print(curr_move)
                        board.push(curr_move)


                # player chose black
                elif(side == "2"):

                    # player's turn
                    if(not board.turn):

                        # get possible moves and put them in a dict for choosing
                        possible_moves = board.legal_moves
                        move_dict = collections.OrderedDict()
                        #print(possible_moves)
                        move_count = 0
                        for move in possible_moves:
                            move_count_string = str(move_count)
                            move_dict[move_count_string] = str(move)

                        # have the player select a move
                        print(move_dict)
                        print("Select a move from above:")
                        player_move = input()
                        player_move_int = int(player_move)
                        while((player_move_int>count)or(player_move_int<1)):
                            print("Move does not exist. Try again...")
                            player_move = input()

                        # make the move
                        curr_move = chess.Move.from_uci(action)
                        #print(curr_move)
                        board.push(curr_move)

                    # AI's turn
                    else:

                        print("The minimax agent is making a move... This could take a while...")

                        #start = timeit.timeit()
                        action = agent.getAction(board)
                        #end = timeit.timeit()
                        #time = (end-start)
                        #print(time)
                        #mean_time.append(time)

                        # make the move
                        curr_move = chess.Move.from_uci(action)
                        #print(curr_move)
                        board.push(curr_move)

            if((side!="1") and (side!="2")):
                print("incorrect input, must select black or white. Try again.")
            elif(side=="1"):
                if(not board.turn):
                    print("Congradulations!!! You Won!!!")
                else:
                    print("Ooh, the minimax agent beat you. That's embarrassing...")
            elif(side=="2"):
                if(board.turn):
                    print("Congradulations!!! You Won!!!")
                else:
                    print("Ooh, the minimax agent beat you. That's embarrassing...")

            print("Average AI move time: ", np.mean(mean_time))
            board.clear()


        # Exit
        elif(option == "3"):
            # ascii art from: https://www.asciiart.eu/holiday-and-events/christmas/santa-claus
            ascii_art="""
                |,\/,| |[_' |[_]) |[_]) \\//
                ||\/|| |[_, ||'\, ||'\,  ||

                        ___ __ __ ____  __  __  ____  _  _    __    __
                       // ' |[_]| |[_]) || ((_' '||' |,\/,|  //\\  ((_'
                       \\_, |[']| ||'\, || ,_))  ||  ||\/|| //``\\ ,_))


                                                     ,;7,
                                                   _ ||:|,
                                 _,---,_           )\'  '|
                               .'_.-.,_ '.         ',')  j
                              /,'   ___}  \        _/   /
                  .,         ,1  .''  =\ _.''.   ,`';_ |
                .'  \        (.'T ~, (' ) ',.'  /     ';',
                \   .\(\O/)_. \ (    _Z-'`>--, .'',      ;
                 \  |   I  _|._>;--'`,-j-'    ;    ',  .'
                __\_|   _.'.-7 ) `'-' "       (      ;'
              .'.'_.'|.' .'   \ ',_           .'\   /
              | |  |.'  /      \   \          l  \ /
              | _.-'   /        '. ('._   _ ,.'   \i
            ,--' ---' / k  _.-,.-|__L, '-' ' ()    ;
             '._     (   ';   (    _-}             |
              / '     \   ;    ',.__;         ()   /
             /         |   ;    ; ___._._____.: :-j
            |           \,__',-' ____: :_____.: :-\
            |               F :   .  ' '        ,  L
            ',             J  |   ;             j  |
              \            |  |    L            |  J
               ;         .-F  |    ;           J    L
                \___,---' J'--:    j,---,___   |_   |
                          |   |'--' L       '--| '-'|
                           '.,L     |----.__   j.__.'
                            | '----'   |,   '-'  }
                            j         / ('-----';
                           { "---'--;'  }       |
                           |        |   '.----,.'
                           ',.__.__.'    |=, _/
                            |     /      |    '.
                            |'= -x       L___   '--,
                      snd   L   __\          '-----'
                             '.____)
            """
            print(ascii_art)
            print("Goodbye!")


        # Non-compatible input
        else:
            print("Incorrect option, try again...")


    return 0


main()
