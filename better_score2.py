import numpy as np
import random
import copy
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
boarder = 15
random.seed(0)
# don't change the class name
score = {
    'ONE':7,
    'TWO': 50,
    'THREE': 150,
    'FOUR': 500,
    'FIVE': 4000,
    'JUMP_TWO':35,
    'JUMP_THREE': 100,
    'DEAD_ONE': 1,
    'DEAD_TWO': 5,
    'DEAD_THREE': 17,
    'DEAD_FOUR': 75,
    'DEAD_JUMP_FOUR':62,
    'DEAD_JUMP_FOUR2':3,
    'DEAD_JUMP_THREE':12,
    'DEAD_JUMP_TWO':2,
    'DEAD': -3
}


# class Point:
#     pointScore = 0
#     x = 0
#     y = 0
#     role = 0
#
#     def __init__(self, x, y, chessboard):
#         self.x = x
#         self.y = y
#         self.role = chessboard[x][y]


class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list.
        # System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        # The input is current chessboard.

    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()

        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        # idx = np.where(chessboard == COLOR_NONE)
        # idx = list(zip(idx[0], idx[1]))
        # pos_idx = random.randint(0, len(idx)-1)
        # new_pos = idx[pos_idx]
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        # assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        # self.candidate_list.append(new_pos)
        if len(self.candidate_list) == 0:
            idx = np.where(chessboard == COLOR_NONE)
            idx = list(zip(idx[0], idx[1]))
            pos_idx = random.randint(0, len(idx) - 1)
            new_pos = idx[pos_idx]
            self.candidate_list.append(new_pos)
        self.minmax(chessboard)
        return self.candidate_list[-1]

    # 判断坐标附近是不是有相邻点
    def hasNeighbor(self, x, y, neighorNum, distance, chessboard):
        xStart = x - distance if x - distance >= 0 else 0
        yStart = y - distance if x - distance >= 0 else 0
        xEnd = x + distance + 1 if x + distance <= boarder else boarder
        yEnd = y + distance + 1 if x + distance <= boarder else boarder
        for i in range(xStart, xEnd):
            if i < 0 or i >= boarder:
                continue
            else:
                for j in range(yStart, yEnd):
                    if j < 0 or j >= boarder: continue
                    if i == x and j == y:
                        continue
                    else:
                        if chessboard[i][j] != COLOR_NONE:
                            neighorNum = neighorNum - 1
                        if neighorNum <= 0:
                            return True
        return False

    # 给每一个角色的每一个棋子打分，仅仅是每一个棋子
    def findPattern(self, chessboard, x, y, role):
        result = 0

        # 纵向计数
        # reset()
        count = 1
        gap = -1
        barrier = 0
        counterCount = 0
        i = y
        while True:
            i = i + 1
            if i >= boarder:
                barrier = barrier + 1
                break
            tempPoint = chessboard[x][i]
            if tempPoint == COLOR_NONE:
                if gap == -1 and i < boarder - 1 and chessboard[x][i + 1] == role:
                    gap = count
                    continue
                else:
                    break
            if tempPoint == role:
                count = count + 1
                continue
            else:
                barrier = barrier + 1
                break
        i = y
        while True:
            i = i - 1
            if i < 0:
                barrier = barrier + 1
                break
            tempPoint = chessboard[x][i]
            if tempPoint == COLOR_NONE:
                if gap == -1 and i > 0 and chessboard[x][i - 1] == role:
                    gap = 0
                    continue
                else:
                    break
            if tempPoint == role:
                counterCount = counterCount + 1
                gap = gap if gap == -1 else gap + 1
                continue
            else:
                barrier = barrier + 1
                break
        count += counterCount
        result += self.makeScore(count, barrier, gap)

        # 横向计数
        count = 1
        gap = -1
        barrier = 0
        counterCount = 0
        # reset()
        i = x
        while True:
            i = i + 1
            if i >= boarder:
                barrier = barrier + 1
                break
            tempPoint = chessboard[i][y]
            if tempPoint == COLOR_NONE:
                if gap == -1 and i < boarder - 1 and chessboard[i + 1][y] == role:
                    gap = count
                    continue
                else:
                    break
            if tempPoint == role:
                count = count + 1
                continue
            else:
                barrier = barrier + 1
                break
        i = x
        while True:
            i = i - 1
            if i < 0:
                barrier = barrier + 1
                break
            tempPoint = chessboard[i][y]
            if tempPoint == COLOR_NONE:
                if gap == -1 and i > 0 and chessboard[i][y] == role:
                    gap = 0
                    continue
                else:
                    break
            if tempPoint == role:
                counterCount = counterCount + 1
                gap = gap if gap == -1 else gap + 1
                continue
            else:
                barrier = barrier + 1
                break
        count += counterCount
        result += self.makeScore(count, barrier, gap)

        # 左下到右上向计数
        # reset()
        count = 1
        gap = -1
        barrier = 0
        counterCount = 0
        i = x
        j = y
        while True:
            i = i + 1
            j = j + 1
            if i >= boarder or j >= boarder:
                barrier = barrier + 1
                break
            tempPoint = chessboard[i][j]
            if tempPoint == COLOR_NONE:
                if gap == -1 and i < boarder - 1 and j < boarder - 1 and chessboard[i + 1][j + 1] == role:
                    gap = count
                    continue
                else:
                    break
            if tempPoint == role:
                count = count + 1
                continue
            else:
                barrier = barrier + 1
                break
        i = x
        j = y
        while True:
            i = i - 1
            j = j - 1
            if i < 0 or j < 0:
                barrier = barrier + 1
                break
            tempPoint = chessboard[i][j]
            if tempPoint == COLOR_NONE:
                if gap == -1 and i > 0 and j > 0 and chessboard[i - 1][j - 1] == role:
                    gap = 0
                    continue
                else:
                    break
            if tempPoint == role:
                counterCount = counterCount + 1
                gap = gap if gap == -1 else gap + 1
                continue
            else:
                barrier = barrier + 1
                break
        count += counterCount
        result += self.makeScore(count, barrier, gap)

        # 左上右下向计数
        count = 1
        gap = -1
        barrier = 0
        counterCount = 0
        # reset()
        i = x
        j = y
        while True:
            i = i - 1
            j = j + 1
            if i < 0 or j >= boarder:
                barrier = barrier + 1
                break
            tempPoint = chessboard[i][j]
            if tempPoint == COLOR_NONE:
                if gap == -1 and i > 0 and j < boarder - 1 and chessboard[i - 1][j + 1] == role:
                    gap = count
                    continue
                else:
                    break
            if tempPoint == role:
                count = count + 1
                continue
            else:
                barrier = barrier + 1
                break
        i = x
        j = y
        while True:
            i = i + 1
            j = j - 1
            if i >= boarder or j < 0:
                barrier = barrier + 1
                break
            tempPoint = chessboard[i][j]
            if tempPoint == COLOR_NONE:
                if gap == -1 and i < boarder - 1 and j > 0 and chessboard[i + 1][j - 1] == role:
                    gap = 0
                    continue
                else:
                    break
            if tempPoint == role:
                counterCount = counterCount + 1
                gap = gap if gap == -1 else gap + 1
                continue
            else:
                barrier = barrier + 1
                break
        count += counterCount

        result += self.makeScore(count, barrier, gap)

        return result

    # 与findPattern对接，规定每一种pattern的分数
    def makeScore(self, count, barrier, gap):
        # 没有空隙00000
        if gap <= 0:
            if count >= 5: return score['FIVE']
            if barrier == 0:
                if count == 4:
                    return score['FOUR']
                elif count == 3:
                    return score['THREE']
                elif count == 2:
                    return score['TWO']
                elif count == 1:
                    return score['ONE']
            elif barrier == 1:
                if count == 4:
                    return score['DEAD_FOUR']
                elif count == 3:
                    return score['DEAD_THREE']
                elif count == 2:
                    return score['DEAD_TWO']
                elif count == 1:
                    return score['DEAD_ONE']
            elif barrier == 2:
                return score['DEAD']
            else:
                return 0
        # 空隙在第一个位置或者倒数第一个0_0000
        elif gap == 1 or gap == count - 1:
            if count >= 6: return score['FIVE']
            if barrier == 0:
                if count >= 4:
                    return score['THREE']
                elif count == 3:
                    return score['JUMP_THREE']
                elif count == 2:
                    return score['JUMP_TWO']
            elif barrier == 1:
                if count >= 4:
                    return score['DEAD_JUMP_FOUR']
                elif count == 3:
                    return score['DEAD_JUMP_THREE']
                elif count == 2:
                    return score['DEAD_JUMP_TWO']
            elif barrier == 2:
                return score['DEAD']
            else:
                return 0
        # 空隙在第二个位置或者倒数第二个00_0000
        elif gap == 2 or gap == count - 2:
            if count >= 7: return score['FIVE']
            if barrier == 0:
                if count >= 4: return score['DEAD_THREE']
            elif barrier == 1:
                if count >= 4: return score['DEAD_TWO']
            elif barrier == 2:
                return score['DEAD']
            else:
                return 0
        elif gap == 3 or gap == count - 3:
            if count >= 8: return score['FIVE']
            if barrier == 0:
                if count >= 4: return score['FOUR']
            elif barrier == 1:
                if count >= 4: return score['THREE']
            elif barrier == 2:
                return score['DEAD']
            else:
                return 0
        elif gap == 4 or gap == count - 4:
            if count >= 9: return score['FIVE']
            if barrier == 0:
                if count >= 4: return score['FOUR']
            elif barrier == 1:
                if count >= 4: return score['THREE']
            elif barrier == 2:
                return score['DEAD']
            else:
                return 0
    # 遍历棋盘所有位置，空白不打分，有棋子的地方就打分并把分数赋值给相应叫色，最后得到全局评估

    def evaluation(self, chessboard, comp_color):
        hum = 0
        comp = 0
        hum_color = self.revers_role(comp_color)
        for i in range(0, boarder):
            for j in range(0, boarder):
                if chessboard[i][j] == comp_color:
                    comp += self.findPattern(chessboard, i, j, comp_color)
                elif chessboard[i][j] == hum_color:
                    hum += self.findPattern(chessboard, i, j, hum_color)
                else:
                    continue
                    # 空白直接跳过
        return comp - hum

    # 角色反转
    def revers_role(self, role):

        if role == COLOR_BLACK:

            return COLOR_WHITE
        elif role == COLOR_WHITE:
            return COLOR_BLACK
        else:
            return COLOR_NONE

    def is_win(self, x, y, chessboard, role):
        count = 1
        counterCount = 0
        i = y
        while True:
            i = i + 1
            if i >= boarder:
                break
            tempPoint = chessboard[x][i]
            if tempPoint == role:
                count = count + 1
                continue
            else:
                break
        i = y
        while True:
            i = i - 1
            if i < 0:
                break
            tempPoint = chessboard[x][i]
            if tempPoint == role:
                counterCount = counterCount + 1
                continue
            else:
                break
        count += counterCount
        if count == 5:
            return True
        # 横向计数
        count = 1
        counterCount = 0
        i = x
        while True:
            i = i + 1
            if i >= boarder:
                break
            tempPoint = chessboard[i][y]
            if tempPoint == role:
                count = count + 1
                continue
            else:
                break
        i = x
        while True:
            i = i - 1
            if i < 0:
                break
            tempPoint = chessboard[i][y]
            if tempPoint == role:
                counterCount = counterCount + 1
                continue
            else:
                break
        count += counterCount
        if count == 5:
            return True
        # 左下到右上向计数
        count = 1
        counterCount = 0
        i = x
        j = y
        while True:
            i = i + 1
            j = j + 1
            if i >= boarder or j >= boarder:
                break
            tempPoint = chessboard[i][j]
            if tempPoint == role:
                count = count + 1
                continue
            else:
                break
        i = x
        j = y
        while True:
            i = i - 1
            j = j - 1
            if i < 0 or j < 0:
                break
            tempPoint = chessboard[i][j]
            if tempPoint == role:
                counterCount = counterCount + 1
                continue
            else:
                break
        count += counterCount
        if count == 5:
            return True

        # 左上右下向计数
        count = 1
        counterCount = 0
        i = x
        j = y
        while True:
            i = i - 1
            j = j + 1
            if i < 0 or j >= boarder:
                break
            tempPoint = chessboard[i][j]
            if tempPoint == role:
                count = count + 1
                continue
            else:
                break
        i = x
        j = y
        while True:
            i = i + 1
            j = j - 1
            if i >= boarder or j < 0:
                break
            tempPoint = chessboard[i][j]
            if tempPoint == role:
                counterCount = counterCount + 1
                continue
            else:
                break
        count += counterCount
        if count == 5:
            return True
        return False

    def minmax(self, chessboard):
        def max_value(x, y, alpha, beta, depth, role):
            chessboard[x][y] = role

            if self.is_win(x, y, chessboard, role):
                chessboard[x][y] = COLOR_NONE
                return float('-inf'), x, y

            if depth <= 0:
                v = self.evaluation(chessboard, self.color)
                # print("minvalue depth:", depth, "corod:(%d,%d)" % (x, y), "value:", v, "role:", role)
                chessboard[x][y] = COLOR_NONE
                return v, x, y

            v = float('-inf')
            new_going_list = set()
            for i in range(x - 1 if x > 0 else 0, x + 2 if x <= boarder - 2 else boarder):
                for j in range(y - 1 if y > 0 else 0, y + 2 if y <= boarder - 2 else boarder):
                    if self.hasNeighbor(i, j, 1, 1, chessboard) and chessboard[i][j] == COLOR_NONE:
                        new_going_list.add((i, j))
            new_going_list = new_going_list.union(going_list)
            new_going_list.remove((x, y))

            for empty_point in new_going_list:
                # print("put", i, j, "as", self.revers_role(role))
                v = max(v, min_value(empty_point[0], empty_point[1], alpha, beta, depth - 1, self.revers_role(role))[0])
                # print("minvalue depth:", depth, "corod:(%d,%d)" % (x, y), "value:", v, "role:", role)
                # print("remove", i, j)
                if v >= beta:
                    chessboard[x][y] = COLOR_NONE
                    return v, x, y
                alpha = max(alpha, v)
            chessboard[x][y] = COLOR_NONE
            return v, x, y

        def min_value(x, y, alpha, beta, depth, role):
            chessboard[x][y] = role

            if self.is_win(x, y, chessboard, role):
                chessboard[x][y] = COLOR_NONE
                return float('inf'), x, y

            if depth <= 0:
                v = self.evaluation(chessboard, self.color)
                # print("minvalue depth:", depth, "corod:(%d,%d)" % (x, y), "value:", v, "role:", role)
                chessboard[x][y] = COLOR_NONE
                return v, x, y

            v = float('inf')
            new_going_list = set()
            for i in range(x - 1 if x > 0 else 0, x + 2 if x <= boarder - 2 else boarder):
                for j in range(y - 1 if y > 0 else 0, y + 2 if y <= boarder - 2 else boarder):
                    if self.hasNeighbor(i, j, 1, 1, chessboard) and chessboard[i][j] == COLOR_NONE:
                        new_going_list.add((i, j))
            new_going_list = new_going_list.union(going_list)
            new_going_list.remove((x, y))
            for empty_point in new_going_list:
                # print("put", i, j, "as", self.revers_role(role))
                v = min(v, max_value(empty_point[0], empty_point[1], alpha, beta, depth - 1, self.revers_role(role))[0])
                # print("minvalue depth:", depth, "corod:(%d,%d)" % (x, y), "value:", v, "role:", role)
                # print("remove", i, j)
                if v <= alpha:
                    chessboard[x][y] = COLOR_NONE
                    return v, x, y
                beta = min(beta, v)
            chessboard[x][y] = COLOR_NONE
            return v, x, y

        bestScore = float('-inf')
        beta = float('inf')
        bestAction = None
        center = int((boarder - 1) / 2)
        going_list = set()

        for i in range(0, boarder):
            for j in range(0, boarder):
                if chessboard[i][j] == COLOR_NONE and self.hasNeighbor(i, j, 1, 1, chessboard):
                    going_list.add((i, j))
        if not going_list:
            bestAction = (center, center)
            self.candidate_list.append(bestAction)
            return
        for empty_point in going_list:
            point = min_value(empty_point[0], empty_point[1], bestScore, beta, 1, self.color)
            if point[0] > bestScore:
                bestScore = point[0]
                bestAction = (point[1], point[2])
                self.candidate_list.append(bestAction)
        return


if __name__ == "__main__":
    # chessboard = np.zeros((boarder,boarder), dtype=np.int)
    # chessboard[0, 0:4] = -1
    # chessboard[1, 0:4] = 1
    # a = AI(15, -1, 16)
    # print("the final:",a.go(chessboard))
    a = [[(0, 0) for i in range(3)] for j in range(5)]
    a[0][0] = (1, 1)

    b = copy.deepcopy(a)
    a[0][1] = (0, 1)
    b[0][0] = (9, 9)
    print(a)
    print(b)
