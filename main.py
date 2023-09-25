import copy
import sys
import pygame
import random
import numpy as np

from constants import *

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TTT GAME - by Shiv')
screen.fill(colorBG)

class Board:

    def __init__(self):
        self.squares = np.zeros((rows, columns))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show=False): # 0 if no win, 1/2 for p1/p2 wins
        # vertical wins
        for col in range(columns):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = colorCIRCLE if self.squares[0][col] == 2 else colorCROSS
                    iPos = (col * squareSize + squareSize // 2, 20)
                    fPos = (col * squareSize + squareSize // 2, height - 20)
                    pygame.draw.line(screen, color, iPos, fPos, lineWidth)
                return self.squares[0][col]

        # horizontal wins
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = colorCIRCLE if self.squares[row][0] == 2 else colorCROSS
                    iPos = (20, row * squareSize + squareSize // 2)
                    fPos = (width - 20, row * squareSize + squareSize // 2)
                    pygame.draw.line(screen, color, iPos, fPos, lineWidth)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = colorCIRCLE if self.squares[1][1] == 2 else colorCROSS
                iPos = (20, 20)
                fPos = (width - 20, height - 20)
                pygame.draw.line(screen, color, iPos, fPos, crossWidth)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = colorCIRCLE if self.squares[1][1] == 2 else colorCROSS
                iPos = (20, height - 20)
                fPos = (width - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, crossWidth)
            return self.squares[1][1]

        # no win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(rows):
            for col in range(columns):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # random
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]

    # minimax algo
    def minimax(self, board, maximizing):

        # terminal case
        case = board.final_state()

        # p1 wins
        if case == 1:
            return 1, None

        # p2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # eval
    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f"AI marking square in {move} with eval: {eval}")

        return move  # row, col


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  # 1-cross  #2-circles
        self.gamemode = 'ai'  # pvp or ai
        self.running = True
        self.show_lines()

    # --- DRAW METHODS ---

    def show_lines(self):
        # bg
        screen.fill(colorBG)

        # vertical
        pygame.draw.line(screen, colorLINE, (squareSize, 0), (squareSize, height), lineWidth)
        pygame.draw.line(screen, colorLINE, (width - squareSize, 0), (width - squareSize, height), lineWidth)

        # horizontal
        pygame.draw.line(screen, colorLINE, (0, squareSize), (width, squareSize), lineWidth)
        pygame.draw.line(screen, colorLINE, (0, height - squareSize), (width, height - squareSize), lineWidth)

    def draw_fig(self, row, col):
        if self.player == 1:
            # first line of cross
            start_desc = (col * squareSize + offset, row * squareSize + offset)
            end_desc = (col * squareSize + squareSize - offset, row * squareSize + squareSize - offset)
            pygame.draw.line(screen, colorCROSS, start_desc, end_desc, crossWidth)
            # second line of cross
            start_asc = (col * squareSize + offset, row * squareSize + squareSize - offset)
            end_asc = (col * squareSize + squareSize - offset, row * squareSize + offset)
            pygame.draw.line(screen, colorCROSS, start_asc, end_asc, crossWidth)

        elif self.player == 2:
            # draw circle
            center = (col * squareSize + squareSize // 2, row * squareSize + squareSize // 2)
            pygame.draw.circle(screen, colorCIRCLE, center, radius, circleWidth)


    # other methods
    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()


def main():
    game = Game()
    board = game.board
    ai = game.ai
    while True:

        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:

                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // squareSize
                col = pos[0] // squareSize

                # human mark sqr
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        # AI initial call
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # update the screen
            pygame.display.update()

            # eval
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()
main()