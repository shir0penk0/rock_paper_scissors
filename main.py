import random
import pyxel
from enum import Enum, auto, IntEnum

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128

MAX_WIN = 3


class Hand(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(Enum):
    WIN = auto()
    LOSE = auto()
    DRAW = auto()


class Status(Enum):
    WAITING = auto()
    BEFORE_GAME = auto()
    AFTER_GAME = auto()


class Counter:
    def __init__(self):
        self.cnt_you = 0
        self.cnt_cpu = 0

    def you_win(self):
        if self.cnt_you < 3:
            self.cnt_you += 1

    def cpu_win(self):
        if self.cnt_cpu < 3:
            self.cnt_cpu += 1

    def is_game_over(self):
        if self.cnt_you >= 3 or self.cnt_cpu >= 3:
            return True


class IStatus:

    def next_state(self):
        pass

    def update(self, st):
        pass

    def draw(self):
        pass


class WaitingStatus(IStatus):
    def __init__(self):
        self.is_complete = False
        self.__hand = None

    def next_state(self):
        if self.is_complete is True:
            return BeforeGameStatus(self.__hand)
        return None

    def update(self, st):
        if pyxel.btnp(pyxel.KEY_1):
            print("waiting status press 1")
            self.is_complete = True
            self.__hand = Hand.ROCK
        elif pyxel.btnp(pyxel.KEY_2):
            print("waiting status press 2")
            self.is_complete = True
            self.__hand = Hand.PAPER
        elif pyxel.btnp(pyxel.KEY_3):
            print("waiting status press 3")
            self.is_complete = True
            self.__hand = Hand.SCISSORS

    def draw(self):
        pyxel.text(40, 40, "1 : Rock", 7)
        pyxel.text(40, 50, "2 : Paper", 7)
        pyxel.text(40, 60, "3 : Scissors", 7)


class BeforeGameStatus(IStatus):
    def __init__(self, hand):
        self.__hand = hand
        self.is_complete = False

    def next_state(self):
        if self.is_complete is True:
            return AfterGameStatus(self.__hand)
        return None

    def update(self, st):
        if pyxel.btnp(pyxel.KEY_1):
            print("before status press 1")
            self.is_complete = True

    def draw(self):
        pyxel.text(40, 40, "TODO", 7)


class AfterGameStatus(IStatus):
    def __init__(self, hand):
        self.__hand = hand
        self.__cpu_hand = random.randint(1, 3)
        self.is_complete = False
        self.__result = None
        self.__open_hands()

    def next_state(self):
        if self.is_complete is True:
            return WaitingStatus()
        return None

    def update(self, st):
        pass

    def draw(self):
        pyxel.text(40, 40, f"YOU : {self.__hand}", 7)
        pyxel.text(40, 50, f"CPU : {self.__cpu_hand}", 7)
        pyxel.text(40, 60, f"{self.__result}", 7)

    def __open_hands(self):

        print(f"your hand : {self.__hand}, cpu hand : {self.__cpu_hand}")
        if self.__hand == Hand.ROCK and self.__cpu_hand == Hand.PAPER:
            self.__result = Result.LOSE
        elif self.__hand == Hand.ROCK and self.__cpu_hand == Hand.SCISSORS:
            self.__result = Result.WIN
        elif self.__hand == Hand.PAPER and self.__cpu_hand == Hand.ROCK:
            self.__result = Result.WIN
        elif self.__hand == Hand.PAPER and self.__cpu_hand == Hand.SCISSORS:
            self.__result = Result.LOSE
        elif self.__hand == Hand.SCISSORS and self.__cpu_hand == Hand.ROCK:
            self.__result = Result.LOSE
        elif self.__hand == Hand.SCISSORS and self.__cpu_hand == Hand.PAPER:
            self.__result = Result.WIN
        else:
            self.__result = Result.DRAW
        print(f"result : {self.__result}")


class App:
    def __init__(self):
        self.st = WaitingStatus()
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Rock Paper Scissors")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.st.update(self.st)
        next_st = self.st.next_state()
        if next_st is not None:
            self.st = next_st

    def draw(self):
        pyxel.cls(0)
        self.text_shadow(10, 10, "Quit : Press Q", 7, 1)

        self.st.draw()

    @staticmethod
    def text_shadow(x, y, s, color, shadow_color):
        pyxel.text(x, y, s, shadow_color)
        pyxel.text(x + 1, y, s, color)


if __name__ == '__main__':
    App()
