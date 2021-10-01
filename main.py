import random
import time

import pyxel
from enum import Enum, auto, IntEnum

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

MAX_WIN = 3


class Hand(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(Enum):
    WIN = auto()
    LOSE = auto()
    DRAW = auto()


class Winner(Enum):
    NOBODY = auto()
    PLAYER = auto()
    CPU = auto()


class Counter:
    def __init__(self, cnt_you, cnt_cpu):
        self.__player_win = cnt_you
        self.__cpu_win = cnt_cpu

    def up(self, result):
        if result == Result.WIN:
            return Counter(self.__player_win + 1, self.__cpu_win)
        elif result == Result.LOSE:
            return Counter(self.__player_win, self.__cpu_win + 1)
        else:
            return self

    def get_winner(self):
        if self.__player_win >= MAX_WIN:
            return Winner.PLAYER
        elif self.__cpu_win >= MAX_WIN:
            return Winner.CPU
        else:
            return Winner.NOBODY

    def reset_if_needed(self):
        if self.__player_win >= MAX_WIN or self.__cpu_win >= MAX_WIN:
            return Counter(0, 0)
        else:
            return self

    def get_player_score(self):
        return self.__player_win

    def get_cpu_score(self):
        return self.__cpu_win


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
            self.__is_complete = True
            self.__hand = Hand.ROCK
        elif pyxel.btnp(pyxel.KEY_2):
            self.__is_complete = True
            self.__hand = Hand.PAPER
        elif pyxel.btnp(pyxel.KEY_3):
            self.__is_complete = True
            self.__hand = Hand.SCISSORS

    def draw(self):
        pyxel.text(31, 15, "Select your hand", 6)
        # Rock
        pyxel.blt(20, 25, 0, 0, 0, 16, 16, colkey=13)
        pyxel.text(27, 42, "1", 7)

        # Paper
        pyxel.blt(55, 25, 0, 32, 0, 16, 16, colkey=13)
        pyxel.text(62, 42, "2", 7)

        # Scissors
        pyxel.blt(90, 25, 0, 16, 0, 16, 16, colkey=13)
        pyxel.text(97, 42, "3", 7)


class BeforeGameStatus(IStatus):
    def __init__(self, hand, counter):
        self.__hand = hand
        self.__is_complete = False
        self.__counter = counter
        self.__x = 0
        self.__open_time = time.monotonic()
        self.__animation_end_time = None

    def get_counter(self):
        return self.__counter

    def next_state(self):
        if self.__is_complete is True:
            return AfterGameStatus(self.__hand, self.__counter)
        return None

    def update(self, st):
        pass

    def draw(self):
        pyxel.blt(0, 17, 1, self.__x, 0, 128, 32, colkey=0)
        # Delay for the animation start
        if time.monotonic() - self.__open_time < 0.8:
            return
        # Scroll image
        if self.__x < 128:
            self.__x += 4
        else:
            # Animation end
            if self.__animation_end_time is None:
                self.__animation_end_time = time.monotonic()
        # Waiting time for moving on the next state
        if self.__animation_end_time is not None and time.monotonic() - self.__animation_end_time > 0.8:
            self.__is_complete = True


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
        # Player's hand
        if self.__hand == Hand.ROCK:
            pyxel.blt(28, 25, 0, 0, 0, 16, 16, colkey=13)
        elif self.__hand == Hand.SCISSORS:
            pyxel.blt(28, 25, 0, 16, 0, 16, 16, colkey=13)
        elif self.__hand == Hand.PAPER:
            pyxel.blt(28, 25, 0, 32, 0, 16, 16, colkey=13)

        # CPU's hand
        if self.__cpu_hand == Hand.ROCK:
            pyxel.blt(85, 25, 0, 0, 0, 16, 16, colkey=13)
        elif self.__cpu_hand == Hand.SCISSORS:
            pyxel.blt(85, 25, 0, 16, 0, 16, 16, colkey=13)
        elif self.__cpu_hand == Hand.PAPER:
            pyxel.blt(85, 25, 0, 32, 0, 16, 16, colkey=13)

        # Result
        if self.__result == Result.WIN:
            pyxel.text(51, 20, "YOU WIN", 3)
        elif self.__result == Result.LOSE:
            pyxel.text(49, 20, "YOU LOSE", 8)
        elif self.__result == Result.DRAW:
            pyxel.text(56, 20, "DRAW", 15)

        # When the game is over
        if self.__counter.get_winner() == Winner.PLAYER:
            pyxel.text(33, 45, "Congratulations!", pyxel.frame_count % 16)
        elif self.__counter.get_winner() == Winner.CPU:
            pyxel.text(55, 45, "Oh...", 3)
        if self.__counter.get_winner() == Winner.NOBODY:
            text_shadow(50, 55, "N : NEXT GAME", 7, 1)
        else:
            text_shadow(50, 55, "N : NEW GAME", 7, 1)

    def __open_hands(self):
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
        print(f"your hand : {self.__hand}, cpu hand : {self.__cpu_hand}, result : {self.__result}")


def text_shadow(x, y, s, color, shadow_color):
    pyxel.text(x, y, s, shadow_color)
    pyxel.text(x + 1, y, s, color)


class App:
    def __init__(self):
        self.st = WaitingStatus(Counter(0, 0))
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Rock Paper Scissors",
                   scale=5, quit_key=pyxel.KEY_Q)
        pyxel.mouse(False)
        pyxel.load("assets/resource.pyxres")
        pyxel.image(1).load(0, 0, "assets/rock_paper_scissors.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.st.update(self.st)
        next_st = self.st.next_state()
        if next_st is not None:
            self.st = next_st

    def draw(self):
        # Clear display to black
        pyxel.cls(0)
        # Message for quit
        text_shadow(5, 55, "Q : QUIT", 7, 1)
        # Display counter
        cnt = self.st.get_counter()
        text_shadow(12, 5, f"YOU WIN : {cnt.get_player_score()}    CPU WIN : {cnt.get_cpu_score()}", 7,
                    1)

        self.st.draw()


if __name__ == '__main__':
    App()
