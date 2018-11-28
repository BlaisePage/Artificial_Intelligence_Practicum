'''

Practicum: Python Chess AI
Authors: Blaise Page
CSCI 3202: Intro to Artificial Intelligence
Professor: Chris Heckman


'''

import chess
import random
from time import sleep


board = chess.Board()


while(not board.is_checkmate()):
    print(board)

    #print(board.legal_moves)
    possible_moves = board.legal_moves

    move_list = []
    print(possible_moves)
    for i in possible_moves:
        move_list.append(str(i))

    rand_num = random.randint(0,len(move_list)-1)
    curr_move = chess.Move.from_uci(move_list[rand_num])
    board.push(curr_move)


    sleep(0.5)


'''

    '''
