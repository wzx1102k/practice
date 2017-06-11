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

    def get_card_edge(self, image_path):
        pass

    def get_card_cost(self, image_path, des_path):
        card_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        card_cost = card_img[0:100, 0:100]
        card_blurred = card_cost
        (T, card_cost) = cv2.threshold(card_blurred, 240, 255, cv2.THRESH_BINARY)

        num_sum = np.zeros((60, 75), np.uint16)
        for i in range(0, 60, 1):
            for j in range(0, 75, 1):
                num_img = card_cost[i:i+40, j:j+25]
                num_sum[i, j] = np.sum(num_img == 255)
        x, y = np.where(num_sum == np.max(num_sum))
        x_pos = x[x.size>>1]
        y_pos = y[y.size>>1]
        card_cost = card_cost[x_pos:x_pos+40, y_pos:y_pos+25]
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
    card_demo.get_card_cost(sys.argv[1], sys.argv[2])