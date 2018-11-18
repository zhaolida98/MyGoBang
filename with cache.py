import numpy as np
import random, copy
import time
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
boarder = 15
random.seed(0)
# don't change the class name
score = {
    'ONE': 10,
    'TWO': 100,
    'THREE': 1000,
    'FOUR': 100000,
    'FIVE': 10000000,
    'DEAD_ONE': 1,
    'DEAD_TWO': 10,
    'DEAD_THREE': 100,
    'DEAD_FOUR': 10000
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
        self.minmax(chessboard)
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
        if len(self.candidate_list) == 0:
            idx = np.where(chessboard == COLOR_NONE)
            idx = list(zip(idx[0], idx[1]))
            pos_idx = random.randint(0, len(idx)-1)
            new_pos = idx[pos_idx]
            self.candidate_list.append(new_pos)
        return self.candidate_list[-1]

    # 判断坐标附近是不是有相邻点
    def hasNeighbor(self, x, y, neighorNum, distance, chessboard):
        xStart = x - distance if x - distance >= 0 else 0
        yStart = y - distance if x - distance >= 0 else 0
        xEnd = x + distance + 1 if x + distance <= boarder else boarder
        yEnd = y + distance + 1 if x + distance <= boarder else boarder
        for i in range(xStart, xEnd):
            if i<0 or i >= boarder: continue
            else:
                for j in range(yStart, yEnd):
                    if j < 0 or j >= boarder: continue
                    if i == x and j == y: continue
                    else:
                        if chessboard[i][j] != COLOR_NONE:
                            neighorNum = neighorNum - 1
                        if neighorNum <= 0:
                            return True
        return False

    # 给每一个角色的每一个棋子打分，仅仅是每一个棋子
    def findPattern(self, chessboard, x, y, role):
        result = 0

        #纵向计数
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
                if gap == -1 and i < boarder - 1 and chessboard[x][i+1] == role :
                    gap = count
                    continue
                else: break
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
                if gap == -1 and i > 0 and chessboard[x][i-1] == role:
                    gap = 0
                    continue
                else: break
            if tempPoint == role:
                counterCount = counterCount + 1
                gap = gap if gap == -1 else gap + 1
                continue
            else:
                barrier = barrier + 1
                break
        count += counterCount
        result += self.makeScore(count, barrier, gap)

        #横向计数
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
                if gap == -1 and i < boarder - 1 and chessboard[i+1][y] == role :
                    gap = count
                    continue
                else: break
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
                else: break
            if tempPoint == role:
                counterCount = counterCount + 1
                gap = gap if gap == -1 else gap + 1
                continue
            else:
                barrier = barrier + 1
                break
        count += counterCount
        result += self.makeScore(count, barrier, gap)

        #左下到右上向计数
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
                if gap == -1 and i < boarder - 1 and j < boarder - 1 and chessboard[i+1][j+1] == role :
                    gap = count
                    continue
                else: break
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
                if gap == -1 and i > 0 and j > 0 and chessboard[i-1][j-1] == role:
                    gap = 0
                    continue
                else: break
            if tempPoint == role:
                counterCount = counterCount + 1
                gap = gap if gap == -1 else gap + 1
                continue
            else:
                barrier = barrier + 1
                break
        count += counterCount
        result += self.makeScore(count, barrier, gap)

        #左上右下向计数
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
                if gap == -1 and i <boarder - 1 and j > 0 and chessboard[i + 1][j - 1] == role:
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
        #没有空隙00000
        if gap <= 0:
            if count >= 5: return score['FIVE']
            if barrier == 0:
                if count == 4: return score['FOUR']
                elif count == 3: return score['THREE']
                elif count == 2: return score['TWO']
                elif count == 1: return score['ONE']
            elif barrier == 1:
                if count == 4: return score['DEAD_FOUR']
                elif count == 3: return score['DEAD_THREE']
                elif count == 2: return score['DEAD_TWO']
                elif count == 1: return score['DEAD_ONE']
            else:
                return 0
        #空隙在第一个位置或者倒数第一个0_0000
        elif gap == 1 or gap == count - 1:
            if count >= 6: return score['FIVE']
            if barrier == 0:
                if count == 5: return score['FOUR']
                elif count == 4: return score['THREE']
                elif count == 3: return score['THREE']
                elif count == 2: return score['TWO']/2
            elif barrier == 1:
                if count == 5: return score['DEAD_FOUR']
                elif count == 4: return score['DEAD_FOUR']
                elif count == 3: return score['DEAD_THREE']
                elif count == 2: return score['DEAD_TWO']
            else:
                return 0
        # 空隙在第二个位置或者倒数第二个00_0000
        elif gap == 2 or gap == count - 2:
            if count >= 7: return score['FIVE']
            if barrier == 0:
                if count == 6: return score['FOUR']
                elif count == 5: return score['THREE']
                elif count == 4: return score['THREE']
                # elif count == 3: return score['ONE']
            elif barrier == 1:
                if count == 6: return score['DEAD_FOUR']
                elif count == 5: return (score['DEAD_THREE']+score['DEAD_TWO'])/2
                elif count == 4: return score['DEAD_TWO']
                # elif count == 3: return score['DEAD_ONE']
            else:
                return 0

        # 空隙在第三个位置或者倒数第三个000_0000
        elif gap == 3 or gap == count - 3:
            if count >= 8: return score['FIVE']
            if barrier == 0:
                if count == 7: return score['FOUR']
                elif count == 6: return score['THREE']
                # elif count == 5: return score['TWO']
                # elif count == 4: return score['ONE']
            elif barrier == 1:
                if count == 7: return score['FOUR']
                elif count == 6: return score['DEAD_FOUR']
                # elif count == 5: return score['DEAD_TWO']
                # elif count == 4: return score['DEAD_ONE']
            else:
                return 0

        # 空隙在第四个位置或者倒数第四个0000_00001
        elif gap == 4 or gap == count - 4:
            if count >= 9: return score['FIVE']
            if barrier == 0:
                if count == 8: return score['FOUR']
                # elif count == 7: return score['THREE']
                # elif count == 6: return score['TWO']
                # elif count == 5: return score['ONE']
            elif barrier == 1:
                if count == 8: return score['FOUR']
                # elif count == 7: return score['DEAD_THREE']
                # elif count == 3: return score['DEAD_TWO']
                # elif count == 2: return score['DEAD_ONE']
            else:
                if count == 8: return score['DEAD_FOUR']
        elif gap == 5 or gap == count - 5:
            return score['FIVE']
    # 遍历棋盘所有位置，空白不打分，有棋子的地方就打分并把分数赋值给相应叫色，最后得到全局评估

    def evaluation(self, chessboard, comp_color, new_score_board):
        hum = 0
        comp = 0
        hum_color = self.revers_role(comp_color)
        for i in range(0, boarder):
            for j in range(0, boarder):
                if chessboard[i][j] == comp_color:
                    comp += new_score_board[i][j][1]
                elif chessboard[i][j] == hum_color:
                    hum += new_score_board[i][j][1]
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

    def is_win(self, x, y,chessboard,role):
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

    def update_score_board(self, x, y, new_score_board, chessboard):

        new_score_board[x][y] = (chessboard[x][y], self.findPattern(chessboard, x, y, chessboard[x][y]))
        #纵向

        i = y
        for counter in range(4):
            i = i + 1
            if i >= boarder:
                break
            tempPoint = chessboard[x][i]
            if tempPoint != COLOR_NONE:
                point_score = self.findPattern(chessboard, x, i, chessboard[x][i])
                new_score_board[x][i] = (chessboard[x][i],point_score)
                continue
            else:
                break
        i = y
        for counter in range(4):
            i = i - 1
            if i < 0:
                break
            tempPoint = chessboard[x][i]
            if tempPoint != COLOR_NONE:
                point_score = self.findPattern(chessboard, x, i, chessboard[x][i])
                new_score_board[x][i] = (chessboard[x][i],point_score)
                continue
            else:
                break

        # 横向计数
        i = x
        for counter in range(4):
            i = i + 1
            if i >= boarder:
                break
            tempPoint = chessboard[i][y]
            if tempPoint != COLOR_NONE:
                point_score = self.findPattern(chessboard, i, y, chessboard[i][y])
                new_score_board[i][y] = (chessboard[i][y],point_score)
                continue
            else:
                break
        i = x
        for counter in range(4):
            i = i - 1
            if i < 0:
                break
            tempPoint = chessboard[i][y]
            if tempPoint != COLOR_NONE:
                point_score = self.findPattern(chessboard, x, i, chessboard[i][y])
                new_score_board[i][y] = (chessboard[i][y],point_score)
                continue
            else:
                break

        # 左下到右上向计数
        i = x
        j = y
        for counter in range(4):
            i = i + 1
            j = j + 1
            if i >= boarder or j >= boarder:
                break
            tempPoint = chessboard[i][j]
            if tempPoint != COLOR_NONE:
                point_score = self.findPattern(chessboard, i, j, chessboard[i][j])
                new_score_board[i][j] = (chessboard[i][j],point_score)
                continue
            else:
                break
        i = x
        j = y
        for counter in range(4):
            i = i - 1
            j = j - 1
            if i < 0 or j < 0:
                break
            tempPoint = chessboard[i][j]
            if tempPoint != COLOR_NONE:
                point_score = self.findPattern(chessboard, i, j, chessboard[i][j])
                new_score_board[i][j] = (chessboard[i][j],point_score)
                continue
            else:
                break

        # 左上右下向计数
        i = x
        j = y
        while True:
            i = i - 1
            j = j + 1
            if i < 0 or j >= boarder:
                break
            tempPoint = chessboard[i][j]
            if tempPoint != COLOR_NONE:
                point_score = self.findPattern(chessboard, i, j, chessboard[i][j])
                new_score_board[i][j] = (chessboard[i][j],point_score)
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
            if tempPoint != COLOR_NONE:
                point_score = self.findPattern(chessboard, i, j, chessboard[i][j])
                new_score_board[i][j] = (chessboard[i][j],point_score)
                continue
            else:
                break
        return new_score_board

    def minmax(self, chessboard):
        def max_value(x, y, alpha, beta, depth, role, score_board):
            chessboard[x][y] = role

            if self.is_win(x, y, chessboard, role):
                chessboard[x][y] = COLOR_NONE
                return float('-inf'), x, y

            new_score_board = copy.deepcopy(score_board)
            new_score_board = self.update_score_board(x, y, new_score_board, chessboard)
            if depth <= 0:
                # 如果深度达到了就总和所有板上的分
                v = self.evaluation(chessboard, self.color, new_score_board)
                # print("minvalue depth:", depth, "corod:(%d,%d)" % (x, y), "value:", v, "role:", role)
                chessboard[x][y] = COLOR_NONE
                return v, x, y

            # 寻找新的going_list
            v = float('-inf')
            new_going_list = set()
            for i in range(x - 1 if x > 0 else 0, x + 2 if x <= boarder - 2 else boarder):
                for j in range(y - 1 if y > 0 else 0, y + 2 if y <= boarder - 2 else boarder):
                    if self.hasNeighbor(i, j, 1, 1, chessboard) and chessboard[i][j] == COLOR_NONE:
                        new_going_list.add((i, j))
            new_going_list = new_going_list.union(going_list)
            new_going_list.difference_update((x,y))

            for empty_point in new_going_list:
                # print("put", i, j, "as", self.revers_role(role))
                v = max(v, min_value(empty_point[0], empty_point[1], alpha, beta, depth - 1, self.revers_role(role), new_score_board)[0])
                # print("minvalue depth:", depth, "corod:(%d,%d)" % (x, y), "value:", v, "role:", role)
                # print("remove", i, j)
                if v >= beta:
                    chessboard[x][y] = COLOR_NONE
                    return v, x, y
                alpha = max(alpha, v)
            chessboard[x][y] = COLOR_NONE
            return v, x, y

        def min_value(x, y, alpha, beta, depth, role, score_board):

            chessboard[x][y] = role

            if self.is_win(x, y, chessboard, role):
                chessboard[x][y] = COLOR_NONE
                return float('inf'), x, y

            new_score_board = copy.deepcopy(score_board)
            new_score_board = self.update_score_board(x, y, new_score_board, chessboard)
            if depth <= 0:
                v = self.evaluation(chessboard, self.color, new_score_board)
                # print("minvalue depth:", depth, "corod:(%d,%d)" % (x, y), "value:", v, "role:", role)
                chessboard[x][y] = COLOR_NONE
                return v, x, y

            v = float('inf')
            new_going_list = set()
            for i in range(x-1 if x>0 else 0, x+2 if x<=boarder-2 else boarder):
                for j in range(y-1 if y>0 else 0, y+2 if y<=boarder-2 else boarder):
                    if self.hasNeighbor(i, j, 1, 1, chessboard) and chessboard[i][j] == COLOR_NONE:
                        new_going_list.add((i,j))
            new_going_list = new_going_list.union(going_list)
            new_going_list.difference_update((x, y))
            for empty_point in new_going_list:
                    # print("put", i, j, "as", self.revers_role(role))
                    v = min(v, max_value(empty_point[0], empty_point[1], alpha, beta, depth - 1, self.revers_role(role), new_score_board)[0])
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
        center = int((boarder-1)/2)
        going_list = set()
        score_board = [[(0,0) for i in range(boarder)] for j in range(boarder)]
        # 确定下一步可走的空格
        for i in range(0, boarder):
            for j in range(0, boarder):
                if chessboard[i][j] == COLOR_NONE and self.hasNeighbor(i, j, 1, 1, chessboard):
                    going_list.add((i,j))
        # 棋盘为空就放在中间
        if not going_list:
            bestAction = (center, center)
            self.candidate_list.append(bestAction)
            return
        # 棋盘不为空先评估
        for i in range(0, boarder):
            for j in range(0, boarder):
                if chessboard[i][j] == COLOR_NONE:
                    score_board[i][j] = (0,0)
                elif chessboard[i][j] == self.color:
                    point_score = self.findPattern(chessboard, i, j, self.color)
                    score_board[i][j] = (self.color, point_score)
                else:
                    counter_color = self.revers_role(self.color)
                    point_score = self.findPattern(chessboard, i, j, counter_color)
                    score_board[i][j] = (counter_color, point_score)

        for empty_point in going_list:
            # print("\r\nthe empty point:",empty_point)
            point = min_value(empty_point[0], empty_point[1], bestScore, beta, 1, self.color,score_board)
            # print("and the point value",point)
            if point[0] > bestScore:
                bestScore = point[0]
                bestAction = (point[1], point[2])
                self.candidate_list.append(bestAction)
        return


if __name__ == "__main__":
    chessboard = np.zeros((boarder,boarder), dtype=np.int)
    chessboard[1, 1:3] = -1
    chessboard[2:4, 3] = -1
    chessboard[1, 6:8] = 1
    chessboard[2:4, 8] = 1
    a = AI(15, -1, 16)
    print("the final:",a.go(chessboard))
