
from keras.models import load_model
from keras.utils import np_utils

import numpy as np
import pygame
import sys
import os


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Board:
    def __init__(self, row=19, col=19):
        self.row = row
        self.col = col
        self.board = np.zeros((row, col))
        self.data = []

    def mark_on_board(self, x_pos, y_pos, turn):
        if self.board[y_pos][x_pos] == 0:
            self.board[y_pos][x_pos] = turn
            self.data.append([x_pos, y_pos])
            return True
        else:
            return False

    def undo(self):
        undo_pos = self.data.pop()
        self.board[undo_pos[1]][undo_pos[0]] = 0
        print("Undo", undo_pos)

    def __check_row(self, x, y):
        turn = self.board[y][x]
        count = 0
        for i in range(1, 5):
            if x+i >= self.row:
                continue
            elif turn == self.board[y][x+i] and self.board[y][x+i] != 0:
                turn = self.board[y][x+i]
                count += 1
        return count == 4

    def __check_col(self, x, y):
        turn = self.board[y][x]
        count = 0
        for i in range(1, 5):
            if y+i >= self.col:
                continue
            elif turn == self.board[y+i][x] and self.board[y+i][x] != 0:
                turn = self.board[y+i][x]
                count += 1
        return count == 4

    def __check_diagonal(self, x, y):
        left_turn = right_turn = self.board[y][x]
        right_side = left_side = 0
        for i in range(1, 5):
            if y+i >= self.col:
                continue
            if x+i < self.row:
                if right_turn == self.board[y+i][x+i] and self.board[y+i][x+i] != 0:
                    right_turn = self.board[y+i][x+i]
                    right_side += 1
            if x-i >= 0:
                if x-i >= 0 and left_turn == self.board[y+i][x-i] and self.board[y+i][x-i] != 0:
                    left_turn = self.board[y+i][x-i]
                    left_side += 1
        return right_side == 4 or left_side == 4

    def check_win(self, turn):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == turn and self.board[y][x] != 0:
                    if self.__check_row(x, y) or self.__check_col(x, y) or self.__check_diagonal(x, y):
                        return True
        return False

    # def check_draw(self):
    #     return np.amin(self.board) != 0

    def save_board(self):
        file_name = 'data.txt'
        file_name = os.path.join(current_path, file_name)
        txt_file = open(file_name, 'a')
        str_data = ''
        for pos in self.data:
            str_data += dec_to_ennea_pos(pos)
        txt_file.write(str_data+'\n')
        txt_file.close()
        print("Save complete.")

    def reset_board(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] != 0:
                    self.board[y][x] = 0
        self.data = []
        print("Reset complete.")


class Tiles:
    def __init__(self, w=20, h=20, row=19, col=19):
        self.w = w
        self.h = h
        self.row = row
        self.col = col
        self.tiles = []
        for y in range(row):
            for x in range(col):
                self.tiles.append(pygame.Rect(w*x, h*y, w, h))

    def check_collide(self, pos):
        for idx, tile in enumerate(self.tiles):
            if tile.collidepoint(pos):
                tile_pos = [idx % self.row, idx//self.row]
                return tile_pos
        return [-1]


def dec_to_ennea_pos(dec_pos):
    ennea = '0123456789abcdefghi'
    ennea_pos = ''
    for pos in dec_pos:
        ennea_pos += ennea[pos % 19]
    return ennea_pos


def draw_marker(screen, board: Board):
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            marker = board.board[i][j]
            if marker != 0:
                color = BLACK if marker == 1 else WHITE
                x = 20 * j + 10
                y = 20 * i + 10
                pygame.draw.circle(screen, color, (x, y), 9)


def get_player(turn):
    return 1 if turn == 1 else 2


def main():
    pygame.init()
    pygame.display.set_caption("오목")
    fps = pygame.time.Clock()
    screen = pygame.display.set_mode((380, 380))

    image_path = os.path.join(current_path, 'gomoku_board.png')

    background = pygame.image.load(image_path)

    board = Board()
    tiles = Tiles()
    turn = 1
    win = False
    # draw = False

    DIR = os.path.join(current_path, 'data')
    game_count = len([name for name in os.listdir(
        DIR) if os.path.isfile(os.path.join(DIR, name))])
    while True:
        # screen.fill(GREY)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if not win:
                    collide_pos = tiles.check_collide(pos)
                    if collide_pos[0] != -1:
                        if board.mark_on_board(collide_pos[0], collide_pos[1], turn):
                            if board.check_win(turn):
                                win = True
                            # elif board.check_draw():
                            #     draw = True
                            else:
                                turn = 1 if turn != 1 else -1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    if win:
                        win = False
                        board.save_board()
                        board.reset_board()
                        turn = 1
                        game_count += 1
                elif event.key == pygame.K_SPACE:
                    if not win:
                        board.undo()
                        turn = 1 if turn != 1 else -1
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         win = False

        draw_marker(screen, board)

        if win:
            font = pygame.font.SysFont('notosanscjkkrblack', 30)
            text = font.render("#{} WIN!".format(
                get_player(turn)), True, BLACK if turn == 1 else WHITE)
            screen.blit(text, (5, 10))

        pygame.display.update()
        fps.tick(30)


if __name__ == "__main__":
    current_path = os.path.dirname(__file__)
    main()
