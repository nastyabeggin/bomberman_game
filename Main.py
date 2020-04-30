from codebattleclient.CodeBattleClient import GameClient
import random
import logging
from math import sqrt

from codebattleclient.internals.TurnAction import TurnAction
from codebattleclient.internals.Board import Board

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.INFO)


tick, time_away = 0, 0
last_moves = []
last_action = None
all_actions = list(TurnAction)
spent_time, time_to_kill = 0, 0
get_away = False
bomb_setted = 0

def get_valid(my_point, board, danger=False):
    '''It finds the least dangerous move'''
    val = []
    left, right, top, bottom = my_point.shift_left(1), my_point.shift_right(1), my_point.shift_top(1), my_point.shift_bottom(1)
    ind = 4
    while val == [] and ind > 0:
        if board.is_free(left):
            if  check_safety(left, board, ind):
                val.append(all_actions[0])
        if board.is_free(right):
            if check_safety(right, board, ind):
                val.append(all_actions[1])
        if board.is_free(top):
            if check_safety(top, board, ind):
                val.append(all_actions[2])
        if board.is_free(bottom):
            if check_safety(bottom, board, ind):
                val.append(all_actions[3])
        ind -= 1
    if len(val) == 0:
        all_bombs = board.get_fast_bombs()
        if board.is_free(left) and left not in all_bombs:
            val.append(all_actions[0])
        if board.is_free(right) and right not in all_bombs:
            val.append(all_actions[1])
        if board.is_free(top) and top not in all_bombs:
            val.append(all_actions[2])
        if board.is_free(bottom) and bottom not in all_bombs:
            val.append(all_actions[3])
    if len(val) == 0 and danger:
        if board.is_free(left):
            val.append(all_actions[0])
        if board.is_free(right):
            val.append(all_actions[1])
        if board.is_free(top):
            val.append(all_actions[2])
        if board.is_free(bottom):
            val.append(all_actions[3])

    return val


def check_safety(point, board, ind=2, b=True):
    '''It checks the bombs and the metchoppers nearby'''
    all_mitchs = board.get_metchoppers()
    all_bombs = board.get_fast_bombs(ind)
    for i in range(4):
        if point.shift_bottom(i) in all_bombs:
            return False
        if point.shift_top(i) in all_bombs:
            return False
        if point.shift_left(i) in all_bombs:
            return False
        if point.shift_right(i) in all_bombs:
            return False
    if b:
        if point.shift_bottom(1) in all_mitchs:
            return False
        if point.shift_top(1) in all_mitchs:
            return False
        if point.shift_left(1) in all_mitchs:
            return False
        if point.shift_right(1) in all_mitchs:
            return False

    return True


def reverse_action(action):
    """It helps us not to repeat the previous """
    if action == all_actions[0]:
        return all_actions[1]
    elif action == all_actions[1]:
        return all_actions[0]
    elif action == all_actions[2]:
        return all_actions[3]
    elif action == all_actions[3]:
        return all_actions[2]
    return all_actions[4]


def reach_target(my_point, target):
    '''What actions should we do to kill the target'''
    mx, my = my_point.get_x(), my_point.get_y()
    tx, ty = target.get_x(), target.get_y()
    val = []
    if mx > tx:
        val.append(all_actions[0])
    elif mx < tx:
        val.append(all_actions[1])
    if my < ty:
        val.append(all_actions[3])
    elif my > ty:
        val.append(all_actions[2])
    return val


def can_we_kill(my_point, target_point, board):
    mx, my = my_point.get_x(), my_point.get_y()
    tx, ty = target_point.get_x(), target_point.get_y()
    flag = True
    if mx == tx and abs(my-ty) < 4:
        for i in range(abs(my-ty)):
            if my > ty:
                if board.is_barrier_at(my_point.shift_top(i)):
                    flag = False
            elif my < ty:
                if board.is_barrier_at(my_point.shift_bottom(i)):
                    flag = False
        return flag
    elif my == ty and abs(mx-tx) < 4:
        for i in range(abs(mx-tx)):
            if mx > tx:
                if board.is_barrier_at(my_point.shift_left(i)):
                    flag = False
            elif mx < tx:
                if board.is_barrier_at(my_point.shift_right(i)):
                    flag = False
        return flag
    return False


def turn(board):
    global tick, last_action, target, spent_time, time_to_kill, get_away, last_moves, time_away, bomb_setted, search_new
    if board.get_bomberman():
        my_point = board.get_bomberman()
        valid_moves = []
        print(get_away, '- away')
        danger = not check_safety(my_point, board, b=False)
        if (((board.am_i_dead() or tick == 0 or spent_time > time_to_kill) and not get_away) or search_new or target != board.get_the_nearest_bomberman()):
            if board.am_i_dead() or tick == 0 or search_new or target != board.get_the_nearest_bomberman():
                search_new = False
                target = board.get_the_nearest_bomberman()
                time_to_kill = int((sqrt((my_point.get_x() - target.get_x()) ** 2 + (my_point.get_y() - target.get_y()) ** 2)) * 2.5)
                spent_time = 0
            else:
                get_away = True
        if spent_time > time_to_kill:
            get_away = True
        tick += 1
        if not get_away:
            spent_time += 1
            useful_moves = reach_target(my_point, target)
            if danger:
                valid_moves = get_valid(my_point, board)
                if len(valid_moves) == 0:
                    valid_moves = get_valid(my_point, board, danger)
            else:
                valid_moves = get_valid(my_point, board)
            if can_we_kill(my_point, target, board) and len(valid_moves) != 0  and not danger:
                action = random.choice(valid_moves)
                search_new = True
                return all_actions[all_actions.index(action) + 5]
            if len(valid_moves) != 0:
                for i in useful_moves:
                    if i in valid_moves:
                        if tick % 10 == 9 and not danger:
                            tick += 1
                            return all_actions[all_actions.index(i) + 5]
                        else:
                            tick += 1
                            return i
                action = random.choice(valid_moves)
                if len(valid_moves) > 1:
                    while action == last_action:
                        action = random.choice(valid_moves)
                if tick % 10 == 1 and not danger:
                    last_action = reverse_action(action)
                    return all_actions[all_actions.index(action) + 5]
                else:
                    last_action = reverse_action(action)
                    return random.choice(valid_moves)
            else:
                pass
        else:
            valid_moves = get_valid(my_point, board)
            time_away += 1
            if len(last_moves) > 2:
                last_moves = [last_moves[-2], last_moves[-1]]
            for i in valid_moves:
                if i not in last_moves:
                    if time_away > 14:
                        get_away = False
                    last_moves.append(reverse_action(i))
                    if time_away % 4 == 3:
                        return all_actions[all_actions.index(i) + 5]
                    else:
                        return i
            try:
                return valid_moves[0]
            except Exception:
                pass




def main():
    a = gcb = GameClient(
        "http://codebattle2020final.westeurope.cloudapp.azure.com/codenjoy-contest/board/player/3pjhi8umx0ei9dhlk2t0?code=8711333452823247871&gameName=bomberman")
    gcb.run(turn)


if __name__ == '__main__':
    main()