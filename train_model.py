import numpy as np
import os


def train_board(positions, x_data, y_data):
    init_boards_x = []
    init_boards_y = []

    for i in range(len(positions)-1):
        init_board_x = np.zeros((19,19))
        init_board_y = np.zeros((19,19))
        for j in range(i+1):
            init_board_x[positions[i][1]][positions[i][0]] = 1 if i%2 == 0 else -1
        init_board_y[positions[i+1][1]][positions[i+1][0]] = 1 if i%2 == 0 else -1

        init_boards_x.append(init_board_x)
        init_boards_y.append(init_board_y)


    flip_boards_x = []
    flip_boards_y = []
    
    for init_board in init_boards_x:
        flip_boards_x.append(np.flipud(init_board))  # flip the board up and down
        flip_boards_x.append(np.fliplr(init_board))  # flip the board left and right
    for init_board in init_boards_y:
        flip_boards_y.append(np.flipud(init_board))
        flip_boards_y.append(np.fliplr(init_board))


    for board_x in np.concatenate((init_boards_x, flip_boards_x), axis=0):
        x_data.append(board_x)
        for i in range(3):
            x_data.append(np.rot90(board_x, i))
    for board_y in np.concatenate((init_boards_y, flip_boards_y), axis=0):
        y_data.append(board_y)
        for i in range(3):
            y_data.append(np.rot90(board_y, i))

            
def array_to_1D(array):
    for i in range(len(array)):
        array[i] = array[i].flatten()

            
X_train = []
Y_train = []

current_path = os.path.dirname(__file__)
DIR = os.path.join(current_path, 'data')
data_count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])


data = []

for i in range(data_count):
    with open(os.path.join(DIR, '{}.txt'.format(i))) as file:
        lines = file.readlines()
        lines = [list(map(int, line.rstrip().split(','))) for line in lines]
        train_board(lines, X_train, Y_train)
        array_to_1D(X_train)
        array_to_1D(Y_train)

# print(type(Y_train[-1]))


import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='tanh'),
    tf.keras.layers.Dense(128, activation='tanh'),
    tf.keras.layers.Dense(361, activation='sigmoid'),
])
print(len(X_train), len(Y_train))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(np.array(X_train), np.array(Y_train), epochs=10)


model.save(os.path.join(current_path, 'gomoku({}).h5'.format(data_count)))


