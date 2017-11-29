import cv2
import sys
import os
import numpy as np

class maze(object):
    def __init__(self):
        self.width = 200
        self.height = 200
        self.line_step = 5
        self.maze = np.zeros([self.width, self.height])

    def resize_maze(self, width, height, line_step):
        list = [width, height]
        if line_step > list.index(min(list))//10:
            return None
        self.width = width
        self.height = height
        self.line_step = line_step
        self.maze = np.zeros([self.width, self.height])

    def save_maze(self, path):
        cv2.imwrite(path, self.maze)


class cell(object):
    def __init__(self, row = 200, col = 200):
        self.row = row
        self.col = col
        self.cell = np.zeros([self.row + 2, self.col + 2])
        self.direction = []
        self.search_end = False
        self.cell_stack = []

    def random_generate(self, x_start=None, y_start=None, x_end=None, y_end=None):
        if x_start != 1 or x_start != self.col \
            or y_start != 1 or y_start != self.row \
            or y_end != 1 or y_end != self.row \
            or x_end != 1 or x_end != self.col:
            x_start = 1
            y_start = np.random.randint(1, self.col + 1)
            x_end = self.row
            y_end = np.random.randint(1, self.col + 1)

        print('x1: %d, y1: %d, x2: %d, y2: %d' %(x_start, y_start, x_end, y_end))
        search_x = x_start
        search_y = y_start
        cell = np.zeros([self.row + 2, self.col + 2])
        cell[0, :] = 1
        cell[:, 0] = 1
        cell[self.row+1, :] = 1
        cell[:, self.col+1] = 1
        cell_x_stack = []
        cell_y_stack = []

        while 1:
            diretion = []
            if len(cell_x_stack) == 0 \
                or not (search_x == cell_x_stack[-1] and search_y == cell_y_stack[-1]):
                cell_x_stack.append(search_x)
                cell_y_stack.append(search_y)
                cell[search_x, search_y] = 1
                print('---------------------')
                print(cell)

            if search_x == x_end and search_y == y_end:
                break

            #print(search_x, search_y)
            if cell[search_x-1, search_y] == 0:
                diretion.append('UP')
            if cell[search_x+1, search_y] == 0:
                diretion.append('DOWN')
            if cell[search_x, search_y-1] == 0:
                diretion.append('LEFT')
            if cell[search_x, search_y+1] == 0:
                diretion.append('RIGHT')

            print('search x : %d, y: %d' % (search_x, search_y))
            print(diretion)
            if len(diretion) == 0 and len(cell_x_stack) <= 1:
                print('Wrong search !!')
                break
            elif len(diretion) == 0:
                print('Dead road, pop back')
                cell_x_stack.pop()
                cell_y_stack.pop()
                search_x = cell_x_stack[-1]
                search_y = cell_y_stack[-1]
            else:
                direct_index = np.random.randint(len(diretion))
                if diretion[direct_index] == 'UP':
                    search_x = search_x - 1
                elif diretion[direct_index] == 'DOWN':
                    search_x = search_x + 1
                elif diretion[direct_index] == 'LEFT':
                    search_y = search_y - 1
                elif diretion[direct_index] == 'RIGHT':
                    search_y = search_y + 1

if __name__ == '__main__':
    cellDemo = cell(8, 8)
    cellDemo.random_generate()


        

