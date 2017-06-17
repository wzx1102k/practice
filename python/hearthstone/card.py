import cv2
import os,sys
import numpy as np

class card(object):
    def __init__(self):
        self.card_type_list = ['secret', 'magic', 'minion', 'weapon']
        self.card_cost = 0
        self.card_hero_list = ['priest', 'warlock', 'mage', 'druid', 'hunter', 'paladin', \
                               'warrior', 'shaman', 'rogue', 'common']
        self.card_level_list = ['white', 'blue', 'green', 'orange', 'purple']
        self.card_name = ''
        self.card_type = 'minion'
        self.card_hero = 'common'
        self.card_level = 'white'
        self.card_img = ''

    def get_card_edge(self, image_path):
        pass

    def get_card_img(self, image_path):
        self.card_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    def get_card_cost(self, des_path):
        #card_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        card_cost = self.card_img[0:100, 0:100]
        card_blurred = card_cost
        (T, card_cost) = cv2.threshold(card_blurred, 240, 255, cv2.THRESH_BINARY)
        double_sum = np.zeros((60, 40), np.uint16)
        for i in range(0, 60, 1):
            for j in range(0, 40, 1):
                num_img = card_cost[i:i+40, j:j+60]
                double_sum[i, j] = np.sum(num_img == 255)
        single_sum = np.zeros((60, 75), np.uint16)
        for i in range(0, 60, 1):
            for j in range(0, 75, 1):
                num_img = card_cost[i:i+40, j:j+25]
                single_sum[i, j] = np.sum(num_img == 255)
        #print(np.max(double_sum), np.max(single_sum))
        # 300 is value for number 1 (min value for all nums)
        if np.max(double_sum) - np.max(single_sum) >= 300:
            des_path1 = des_path[:-4] + '_1.png'
            des_path2 = des_path[:-4] + '_2.png'
            y,x = np.where(double_sum == np.max(double_sum))
            x_double = x[x.size>>1]
            y_double = y[y.size>>1]
            y, x = np.where(single_sum == np.max(single_sum))
            x_single = x[x.size>>1]
            y_single = y[y.size>>1]
            #check x_single is rigth or left of x_double
            if x_single > x_double + 10:
                card_double = card_cost[y_double:y_double + 40, 0:x_double+30]
                left_sum = np.zeros((1, x_double+5), np.uint16)
                for i in range(0, x_double+5):
                    num_img = card_double[:, i:i + 25]
                    left_sum[:, i] = np.sum(num_img == 255)
                y, x = np.where(left_sum == np.max(left_sum))
                x_pos = x[x.size >> 1]
                card_cost_1 = card_double[:, x_pos:x_pos + 25]
                card_cost_2 = card_cost[y_single:y_single + 40, x_single:x_single + 25]
            else:
                card_cost_1 = card_cost[y_single:y_single + 40, x_single:x_single + 25]
                card_double = card_cost[y_double:y_double + 40, x_double+30:100]
                right_sum = np.zeros((1, 45-x_double), np.uint16)
                for i in range(0, 45-x_double):
                    num_img = card_double[:, i:i + 25]
                    right_sum[:, i] = np.sum(num_img == 255)
                y, x = np.where(right_sum == np.max(right_sum))
                x_pos = x[x.size >> 1] + x_double + 30
                card_cost_2 = card_double[:, x_pos:x_pos + 25]
            card_cost_1 = cv2.resize(card_cost_1, (5, 8))
            card_cost_2 = cv2.resize(card_cost_2, (5, 8))
            cv2.imwrite(des_path1, card_cost_1)
            cv2.imwrite(des_path2, card_cost_2)
        else:
            y, x = np.where(single_sum == np.max(single_sum))
            x_pos = x[x.size>>1]
            y_pos = y[y.size>>1]
            card_cost = card_cost[y_pos:y_pos+40, x_pos:x_pos+25]
            card_cost = cv2.resize(card_cost, (10, 16))
            cv2.imwrite(des_path, card_cost)

class magic_card(card):
    def __init__(self):
        super(magic_card, self).__init__()

class secret_card(card):
    def __init__(self):
        super(secret_card, self).__init__()

class weapon_card(card):
    def __init__(self):
        super(weapon_card, self).__init__()
        self.attack_value = 0
        self.attack_cnt = 0

class minion_card(card):
    def __init__(self):
        super(minion_card, self).__init__()
        self.attack_value = 0
        self.defence_value = 0
        self.effect_list = ['windfury', 'battlecry', 'deathrattle', 'blessing']

if __name__ == '__main__':
    card_demo = card()
    card_demo.get_card_img(sys.argv[1])
    card_demo.get_card_cost(sys.argv[2])