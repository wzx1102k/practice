import cv2
import sys
import os
import numpy as np

class maze(object):
    def __init__(self, width = 200, height = 200, line_step = 10):
        self.width = width
        self.heigth = height
        self.line_step = line_step
        self.cell_row = self.heigth // self.line_step
        self.cell_col = self.width // self.line_step
        self.maze = np.ones([self.heigth + 1, self.width + 1]) * 255
        self.solution = np.ones([self.heigth + 1, self.width + 1]) * 255
        for i in range(0, self.heigth + 1):
            if i%self.line_step == 0:
                self.maze[i, :] = 0
                self.solution[i, :] = 0

        for i in range(0, self.width + 1):
            if i%self.line_step == 0:
                self.maze[:, i] = 0
                self.solution[:, i] = 0

    def maze_generate(self, x_start=None, y_start=None, x_end=None, y_end=None, cell_path=None, solution_path=None):
        if x_start != 1 and x_end != self.cell_col:
            x_start = 1
            y_start = np.random.randint(1, self.cell_col + 1)
            x_end = self.cell_row
            y_end = np.random.randint(1, self.cell_col + 1)

        self.maze[0, (y_start-1)*self.line_step : y_start*self.line_step] = 255
        self.maze[self.width, (y_end-1)*self.line_step : y_end*self.line_step] = 255
        self.solution[0, (y_start-1)*self.line_step : y_start*self.line_step] = 255
        self.solution[self.width, (y_end-1)*self.line_step : y_end*self.line_step] = 255


        print('x1: %d, y1: %d, x2: %d, y2: %d' %(x_start, y_start, x_end, y_end))
        self.solution[0:self.line_step//2, y_start*self.line_step - self.line_step//2] = 100
        self.solution[self.heigth - self.line_step//2:self.heigth, y_end*self.line_step - self.line_step//2] = 100
        search_x = x_start
        search_y = y_start
        cell = np.zeros([self.cell_row + 2, self.cell_col + 2])
        cell[0, :] = 1
        cell[:, 0] = 1
        cell[self.cell_row+1, :] = 1
        cell[:, self.cell_col+1] = 1
        cell_x_stack = []
        cell_y_stack = []
        solution_end = 0

        while 1:
            diretion = []
            if len(cell_x_stack) == 0 \
                or not (search_x == cell_x_stack[-1] and search_y == cell_y_stack[-1]):
                cell_x_stack.append(search_x)
                cell_y_stack.append(search_y)
                cell[search_x, search_y] = 1
                #print('---------------------')
                #print(cell)

            if search_x == x_end and search_y == y_end:
                solution_end = 1
            #    break

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
                print('End search !!')
                break
            elif len(diretion) == 0:
                print('Dead road, pop back')
                search_x_old = cell_x_stack.pop()
                search_y_old = cell_y_stack.pop()
                search_x = cell_x_stack[-1]
                search_y = cell_y_stack[-1]
                if solution_end == 0:
                    print('*********************************')
                    print('x_old:%d, x: %d, y_old: %d, y: %d' % (search_x_old, search_x, search_y_old, search_y))
                    print('*********************************')
                    if search_y - search_y_old == 0:
                        if search_x > search_x_old:
                            self.solution[(search_x_old * self.line_step - self.line_step // 2) \
                                : (search_x_old * self.line_step + self.line_step // 2 + 1), \
                                search_y * self.line_step - self.line_step // 2] = 255
                        else:
                            self.solution[(search_x * self.line_step - self.line_step // 2) \
                                : (search_x * self.line_step + self.line_step // 2 + 1), \
                                search_y * self.line_step - self.line_step // 2] = 255
                    else:
                        if search_y > search_y_old:
                            self.solution[search_x * self.line_step - self.line_step // 2, \
                                (search_y_old * self.line_step - self.line_step // 2) \
                                : (search_y_old * self.line_step + self.line_step // 2 + 1)] = 255
                        else:
                            self.solution[search_x * self.line_step - self.line_step // 2, \
                                (search_y * self.line_step - self.line_step // 2) \
                                : (search_y * self.line_step + self.line_step // 2 + 1)] = 255
            else:
                direct_index = np.random.randint(len(diretion))
                if diretion[direct_index] == 'UP':
                    search_x = search_x - 1
                    self.maze[search_x * self.line_step, \
                        (search_y - 1) * self.line_step + 1: search_y * self.line_step] = 255
                    self.solution[search_x * self.line_step, \
                        (search_y - 1) * self.line_step + 1: search_y * self.line_step] = 255
                    if solution_end == 0:
                        self.solution[(search_x*self.line_step - self.line_step//2) \
                            : (search_x*self.line_step + self.line_step//2 + 1), \
                            search_y*self.line_step - self.line_step//2] = 100
                elif diretion[direct_index] == 'DOWN':
                    self.maze[search_x * self.line_step, \
                        (search_y - 1) * self.line_step + 1: search_y * self.line_step] = 255
                    self.solution[search_x * self.line_step, \
                    (search_y - 1) * self.line_step + 1: search_y * self.line_step] = 255
                    if solution_end == 0:
                        self.solution[(search_x * self.line_step - self.line_step // 2) \
                            : (search_x * self.line_step + self.line_step // 2 + 1), \
                            search_y * self.line_step - self.line_step // 2] = 100
                    search_x = search_x + 1
                elif diretion[direct_index] == 'LEFT':
                    search_y = search_y - 1
                    self.maze[(search_x-1) * self.line_step + 1: search_x * self.line_step, \
                        search_y * self.line_step] = 255
                    self.solution[(search_x - 1) * self.line_step + 1: search_x * self.line_step, \
                    search_y * self.line_step] = 255
                    if solution_end == 0:
                        self.solution[search_x*self.line_step - self.line_step//2, \
                            (search_y * self.line_step - self.line_step // 2) \
                            : (search_y * self.line_step + self.line_step // 2 + 1)] = 100
                elif diretion[direct_index] == 'RIGHT':
                    self.maze[(search_x - 1) * self.line_step + 1: search_x * self.line_step, \
                        search_y * self.line_step] = 255
                    self.solution[(search_x - 1) * self.line_step + 1: search_x * self.line_step, \
                    search_y * self.line_step] = 255
                    if solution_end == 0:
                        self.solution[search_x * self.line_step - self.line_step // 2, \
                            (search_y * self.line_step - self.line_step // 2) \
                            : (search_y * self.line_step + self.line_step // 2 + 1)] = 100
                    search_y = search_y + 1
        #cv2.imshow('maze', self.maze)
        #cv2.waitKey(0)

        #colorful solution matrix  to rgb
        b = self.solution[:]
        g = self.solution[:]
        r = self.solution[:]

        b = (b!=100) * b
        g = (g!=100) * g
        r = (r!=100) * r + 255 * (r==100)
        solution_rgb = cv2.merge([b, g, r])


        if cell_path != None:
            cv2.imwrite(cell_path, self.maze)
        if solution_path != None:
            cv2.imwrite(solution_path, solution_rgb)


if __name__ == '__main__':
    cnt = sys.argv[1]
    MAZE_PATH = './maze/'
    SOLUTION_PATH = './solution/'
    for i in range(int(cnt)):
        MAZE_NAME = str(i) + '.png'
        mazeDemo = maze(width=200, height=200, line_step=10)
        mazeDemo.maze_generate(cell_path=MAZE_PATH+MAZE_NAME, solution_path=SOLUTION_PATH+MAZE_NAME)


        

