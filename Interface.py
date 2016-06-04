# coding=utf-8
"""
@author : somebody
@date : 03/06/16

@project : XCS
@file : Interface

@Class description :
"""

# coding=utf-8
"""
@author : somebody
@date : 12/05/16

@project : LCStage
@file : Interface

@Class description : This class allow communications between LCSs and the class Maze.
"""


class Maze(object):
    def __init__(self):
        self.matrice = []
        self.height = 8
        self.lenght = 8
        self.posx = 0
        self.posy = 0
        self.food = 10
        self.water = 10
        self.matrice = [['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                        ['-1', '2', '0', '0', '2', '0', '-1', '-1'],
                        ['-1', '0', '-1', '2', '0', '0', '0', '-1'],
                        ['-1', '2', '0', '0', '2', '-1', '0', '-1'],
                        ['-1', '0', '0', '2', '0', '0', '2', '-1'],
                        ['-1', '2', '-1', '0', '-1', '0', '0', '-1'],
                        ['-1', '0', '0', '2', '0', '2', '-1', '-1'],
                        ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']]
        self.introduiceRobot()
        self.env = self.returnPerception(self.posx, self.posy)
        self.perception = self.returnPerception(self.posx, self.posy) + [self.food] + [self.water]
        self.flag = False
        self.letalR = -1000

    def stop(self):
        self.introduiceRobot()
        self.perception = self.returnPerception(self.posx, self.posy)
        self.food = 10
        self.water = 10
        self.flag = False
        self.perception = self.returnPerception(self.posx, self.posy) + [self.food] + [self.water]

    def returnPerception(self, posx, posy):
        return [self.matrice[posx][posy - 1], self.matrice[posx - 1][posy], self.matrice[posx][posy + 1],
                self.matrice[posx + 1][posy]]

    def introduiceRobot(self):
        if self.matrice[6][1] == '0':
            self.posx = self.height - 2
            self.posy = 1
        else:
            posx = None
            posy = None

    def getValuePositionRobot(self):
        return self.matrice[self.posx][self.posy]

    def get_reward(self):
        """
        prévoir eop
        :return:
        """
        pass

    def eop(self):
        if self.flag:
            return True
        else:
            return False

    def execute_action(self, action):
        # type: (Int, Maze) -> object
        """
        :return:
        :param action: 0 = left; 1 = top; 2 = right; 3 = down
        """
        if action == 0:
            if self.perception[0] != '-1':
                # Don't change posx
                self.posy += -1
        elif action == 1:
            if self.perception[1] != '-1':
                self.posx += -1
                # Don't change posy
        elif action == 2:
            if self.perception[2] != '-1':
                # Don't change posx
                self.posy += 1
        elif action == 3:
            if self.perception[3] != '-1':
                self.posx += 1
                # Don't change posy

        value = int(self.getValuePositionRobot())

        if value == 2:
            if self.water < 10:
                self.water += 1
                self.food += 1
        elif value == 0:
            self.food -= 1
            self.water -= 1
            if self.food == 0 or self.water == 0:
                self.flag = True
                return self.letalR

        self.perception = self.returnPerception(self.posx, self.posy) + [self.food] + [self.water]

        return self.reward(value)

    def reward(self, value):
        if value == 0:
            return 0
        if value == 2:
            self.flag = True
            return 2000


