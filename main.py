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
    def __init__(self, cnt_you, cnt_cpu):
        self.__cnt_player = cnt_you
        self.__cnt_cpu = cnt_cpu

    def up(self, result):
        if result == Result.WIN:
            return Counter(self.__cnt_player + 1, self.__cnt_cpu)
        elif result == Result.LOSE:
            return Counter(self.__cnt_player, self.__cnt_cpu + 1)
        else:
            return self

    def is_game_over(self):
        if self.__cnt_player >= 3 or self.__cnt_cpu >= 3:
            return True

    def reset_if_needed(self):
        if self.__cnt_player >= 3 or self.__cnt_cpu >= 3:
            return Counter(0, 0)
        return self

    def get_player_score(self):
        return self.__cnt_player

    def get_cpu_score(self):
        return self.__cnt_cpu


class IStatus:

    def next_state(self):
        pass

    def get_counter(self):
        pass

    def update(self, st):
        pass

    def draw(self):
        pass


class WaitingStatus(IStatus):
    def __init__(self, counter):
        self.__is_complete = False
        self.__hand = None
        self.__counter = counter.reset_if_needed()

    def get_counter(self):
        return self.__counter

    def next_state(self):
        if self.__is_complete is True:
            return BeforeGameStatus(self.__hand, self.__counter)
        return None

    def update(self, st):
        if pyxel.btnp(pyxel.KEY_1):
            print("waiting status press 1")
            self.__is_complete = True
            self.__hand = Hand.ROCK
        elif pyxel.btnp(pyxel.KEY_2):
            print("waiting status press 2")
            self.__is_complete = True
            self.__hand = Hand.PAPER
        elif pyxel.btnp(pyxel.KEY_3):
            print("waiting status press 3")
            self.__is_complete = True
            self.__hand = Hand.SCISSORS

    def draw(self):
        pyxel.text(40, 40, "1 : Rock", 7)
        pyxel.text(40, 50, "2 : Paper", 7)
        pyxel.text(40, 60, "3 : Scissors", 7)


class BeforeGameStatus(IStatus):
    def __init__(self, hand, counter):
        self.__hand = hand
        self.__is_complete = False
        self.__counter = counter

    def get_counter(self):
        return self.__counter

    def next_state(self):
        if self.__is_complete is True:
            return AfterGameStatus(self.__hand, self.__counter)
        return None

    def update(self, st):
        if pyxel.btnp(pyxel.KEY_1):
            print("before status press 1")
            self.__is_complete = True

    def draw(self):
        pyxel.text(40, 40, "TODO", 7)


class AfterGameStatus(IStatus):
    def __init__(self, hand, counter):
        self.__hand = hand
        self.__cpu_hand = random.randint(1, 3)
        self.__is_complete = False
        self.__result = None
        self.__open_hands()
        self.__counter = counter.up(self.__result)

    def get_counter(self):
        return self.__counter

    def next_state(self):
        if self.__is_complete is True:
            return WaitingStatus(self.__counter)
        return None

    def update(self, st):
        if pyxel.btnp(pyxel.KEY_N):
            self.__is_complete = True

    def draw(self):
        pyxel.text(40, 40, f"YOU : {self.__hand}", 7)
        pyxel.text(40, 50, f"CPU : {self.__cpu_hand}", 7)
        pyxel.text(40, 60, f"{self.__result}", 7)
        text_shadow(40, 100, "PRESS N : NEXT GAME", 7, 1)

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

def text_shadow(x, y, s, color, shadow_color):
    pyxel.text(x, y, s, shadow_color)
    pyxel.text(x + 1, y, s, color)


class App:
    def __init__(self):
        self.st = WaitingStatus(Counter(0, 0))
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
        # Clear display to black
        pyxel.cls(0)
        # Message for quit
        text_shadow(10, 10, "Quit : Press Q", 7, 1)
        # Display counter
        cnt = self.st.get_counter()
        text_shadow(10, 20, f"YOU WIN : {cnt.get_player_score()}    CPU WIN : {cnt.get_cpu_score()}", 7,
                         1)

        self.st.draw()



if __name__ == '__main__':
    App()
