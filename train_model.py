import numpy as np
import os



# increase amount of board (1 -> 12)
def flip_rotate(board, data):
    for board_to_rotate in [board, np.flipud(board), np.fliplr(board)]:
        data.append(board_to_rotate)
        for i in range(3):
            data.append(np.rot90(board_to_rotate, i))


def train_board(positions, x_data, y_data):
    winner = 0 if len(positions)%2 == 1 else 1
    for i in range(1+winner, len(positions)-1, 2):
        board_x = np.zeros((19,19))
        board_y = np.zeros((19,19))

        for j in range(i+1):
            board_x[positions[j][1]][positions[j][0]] = 1 if j%2 == 0 else -1

        board_y[positions[i+1][1]][positions[i+1][0]] = 1

        flip_rotate(board_x, x_data)
        flip_rotate(board_y, y_data)


def array_to_1D(array):
    for i in range(len(array)):
        array[i] = array[i].flatten()

        
def ennea_to_dec(ennea):
    ennea_list = '0123456789abcdefghi'
    return ennea_list.find(ennea)

X_train = []
Y_train = []

current_path = os.path.dirname(__file__)

with open(os.path.join(current_path, 'data.txt')) as file:
    lines = file.readlines()
    data = []
    for line in lines:
        board_data = []
        line = line[:-1]
        for i in range(0, len(line), 2):
            board_data.append(
                [ennea_to_dec(line[i]), ennea_to_dec(line[i+1])])
        train_board(board_data, X_train, Y_train)
        data.append(board_data)
    data_count = len(data)
array_to_1D(Y_train)

# print(X_train[-1], data_count)


import tensorflow as tf
from tensorflow.keras import datasets, layers, models

X_train = np.array(X_train).reshape(len(X_train), 19,19,1)
model = models.Sequential([
    layers.Conv2D(64, 7, padding='same', activation='relu', input_shape=(19, 19, 1)),
    layers.Conv2D(1, 1, padding='same', activation=None),
    layers.Reshape((361,)),
    layers.Activation('softmax')
])
model.summary()

print(len(X_train), len(Y_train))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(np.array(X_train), np.array(Y_train), epochs=30)

model.save(os.path.join(current_path, 'gomoku({}).h5'.format(data_count)))

