# coding=utf-8
"""
@author : somebody
@date : 03/06/16

@project : XCS
@file : Interface

@Class description :
"""
import curses

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
        self.mouv = False
        self.matrice = []
        self.height = 8
        self.lenght = 8
        self.posx = 0
        self.posy = 0
        self.food = 15
        self.water = 15
        self.matrice = [['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                        ['-1', '2', '0', '0', '2', '2', '-1', '-1'],
                        ['-1', '0', '-1', '-1', '2', '0', '2', '-1'],
                        ['-1', '2', '0', '2', '0', '-1', '2', '-1'],
                        ['-1', '0', '2', '0', '2', '0', '2', '-1'],
                        ['-1', '0', '0', '2', '-1', '0', '0', '-1'],
                        ['-1', '0', '2', '0', '0', '2', '-1', '-1'],
                        ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']]
        self.introduiceRobot()
        self.env = self.returnPerception(self.posx, self.posy)
        self.perception = self.env + [self.food] #+ [self.water]
        self.flag = False
        self.letalR = -3000

    def stop(self):
        self.introduiceRobot()
        self.perception = self.returnPerception(self.posx, self.posy)
        self.food = 15
        self.water = 15
        self.flag = False
        self.perception = self.returnPerception(self.posx, self.posy) + [self.food]# + [self.water]

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

    def execute_action(self, action):
        # type: (Int, Maze) -> object
        #assert 0 < self.posx < 7, "Wrong posx"
        #assert 0 < self.posy < 7, "Wrong posy"

        """
        :return:
        :param action: 0 = left; 1 = top; 2 = right; 3 = down
        """
        self.mouv = False
        if action == 0 and int(self.perception[0]) > -1 and 0 < self.posy - 1 < 7:
            # Don't change posx
            self.posy += -1
            self.mouv = True
        if action == 1 and int(self.perception[1]) > -1 and 0 < self.posx - 1 < 7:
            self.posx += -1
            self.mouv = True
            # Don't change posy
        if action == 2 and int(self.perception[2]) > -1 and 0 < self.posy + 1 < 7:
            # Don't change posx
            self.posy += 1
            self.mouv = True
        if action == 3 and int(self.perception[3]) > -1 and 0 < self.posx + 1 < 7:
            self.posx += 1
            # Don't change posy
            self.mouv = True

        value = int(self.getValuePositionRobot())

        if value == 2:
            if self.food < 15 and self.mouv:
                self.food += 3
                return 2000
            return 0
        # elif value == 1:
        #     if self.water < 15 and self.mouv:
        #         self.water += 4
        #         return 2000
        #     return 100
        elif value == 0:
            self.food -= 1
            # self.water -= 1
            if self.food == 0: # or self.water == 0:
                self.flag = True
                self.stop()
                return self.letalR

        self.perception = self.returnPerception(self.posx, self.posy) + [self.food] #+ [self.water]

        return 0

    def __getattr__(self, item):
        return item


class PlayMaze(object):
    def __init__(self, posx=1, posy=1):
        self.matrice = [['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'],
                        ['-1', '2', '0', '0', '2', '2', '-1', '-1'],
                        ['-1', '0', '-1', '-1', '2', '0', '2', '-1'],
                        ['-1', '2', '0', '2', '0', '-1', '2', '-1'],
                        ['-1', '0', '2', '0', '2', '0', '2', '-1'],
                        ['-1', '2', '0', '2', '-1', '2', '0', '-1'],
                        ['-1', '0', '0', '2', '0', '2', '-1', '-1'],
                        ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']]
        self.posx = posx
        self.posy = posy
        self.getValue = 0
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

    def setValuePositionRobot(self):
        self.getValue = self.matrice[self.posx][self.posy]
        self.matrice[self.posx][self.posy] = 'X'

    def restoreValue(self):
        self.matrice[self.posx][self.posy] = self.getValue

    def play(self, posx, posy, str1, str2):
        if self.matrice[self.posx][self.posy] == 'X':
            self.restoreValue()
        self.posx = posx
        self.posy = posy
        self.setValuePositionRobot()
        self.stdscr.addstr(0, 0, str(self.matrice[0]).replace(",", " ").replace("'", ""))
        self.stdscr.addstr(1, 0, str(self.matrice[1]).replace(",", " ").replace("'", "").replace("0", " 0").replace("2",
                                                                                                                    " 2").replace(
            "X", " X").replace("1", " 1"))
        self.stdscr.addstr(2, 0, str(self.matrice[2]).replace(",", " ").replace("'", "").replace("0", " 0").replace("2",
                                                                                                                    " 2").replace(
            "X", " X").replace("1", " 1"))
        self.stdscr.addstr(3, 0, str(self.matrice[3]).replace(",", " ").replace("'", "").replace("0", " 0").replace("2",
                                                                                                                    " 2").replace(
            "X", " X").replace("1", " 1"))
        self.stdscr.addstr(4, 0, str(self.matrice[4]).replace(",", " ").replace("'", "").replace("0", " 0").replace("2",
                                                                                                                    " 2").replace(
            "X", " X").replace("1", " 1"))
        self.stdscr.addstr(5, 0, str(self.matrice[5]).replace(",", " ").replace("'", "").replace("0", " 0").replace("2",
                                                                                                                    " 2").replace(
            "X", " X").replace("1", " 1"))
        self.stdscr.addstr(6, 0, str(self.matrice[6]).replace(",", " ").replace("'", "").replace("0", " 0").replace("2",
                                                                                                                    " 2").replace(
            "X", " X").replace("1", " 1"))
        self.stdscr.addstr(7, 0, str(self.matrice[7]).replace(",", " ").replace("'", ""))
        self.stdscr.addstr(8, 0, str1)
        self.stdscr.addstr(9, 0, str2)

        self.stdscr.refresh()

    def __getattr__(self, item):
        return item
