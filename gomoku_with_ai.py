
from keras.models import load_model
import random
import pygame
import sys
import os
from gomoku import Board, Tiles, draw_marker, get_player

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def switch_turn(turn):
    return 1 if turn != 1 else -1


def init_markers(turn):
    if turn != 1:
        while True:
            pos = [random.randint(8, 10), random.randint(8, 10)]
            if pos != [9, 9]:
                break
        return pos
    else:
        return [9, 9]


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
    user_turn = -1
    ai_turn = 1
    win = False
    # draw = False

    DIR = os.path.join(current_path, 'models')
    model = load_model(os.path.join(DIR, 'gomoku(22)_(acc56%).h5'))

    while True:
        # screen.fill(GREY)
        screen.blit(background, (0, 0))

        if turn == ai_turn and not win:
            count = 0
            if len(board.data) == 1 or len(board.data) == 0:
                pos = init_markers(turn)
                board.mark_on_board(pos[0], pos[1], turn)
                turn = switch_turn(turn)
            else:
                predict_board = board.board.reshape(1, 19, 19, 1)
                predict = model.predict(predict_board)
                while True:
                    index = (-predict).argsort()[0][count]
                    # print(index)
                    if board.mark_on_board(index % 19, index//19, turn):
                        if board.check_win(turn):
                            win = True
                        turn = switch_turn(turn)
                        break
                    else:
                        print(index % 19, index//19)
                        count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if turn == user_turn and not win:
                    collide_pos = tiles.check_collide(pos)
                    if collide_pos[0] != -1:
                        if board.mark_on_board(collide_pos[0], collide_pos[1], turn):
                            if board.check_win(turn):
                                win = True
                            else:
                                turn = switch_turn(turn)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    if win:
                        win = False
                        board.reset_board()
                        turn = 1

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
