import numpy as np
import os



# increase amount of board (1 -> 12)
def flip_rotate(board, data):
    for board_to_rotate in [board, np.flipud(board), np.fliplr(board)]:
        data.append(board_to_rotate)
        for i in range(3):
            data.append(np.rot90(board_to_rotate, i))


def train_board(positions, x_data, y_data):
    for i in range(1, len(positions)-1):
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


X_train = []
Y_train = []

current_path = os.path.dirname(__file__)
DIR = os.path.join(current_path, 'data')
data_count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])


for i in range(data_count):
    with open(os.path.join(DIR, '{}.txt'.format(i))) as file:
        lines = file.readlines()
        lines = [list(map(int, line.rstrip().split(','))) for line in lines]
        train_board(lines, X_train, Y_train)
array_to_1D(Y_train)

# print(X_train[-1])


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

