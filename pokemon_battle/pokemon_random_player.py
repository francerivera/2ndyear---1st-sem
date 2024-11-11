import random


def roll_dice():
    return random.randint(1, 6)


class DiceGame:
    def __init__(self):
        self.p1 = 0
        self.p2 = 0

    def play(self):
        while True:
            self.p1, self.p2 = roll_dice(), roll_dice()
            print(f"Player 1 rolls: {self.p1}\nPlayer 2 rolls: {self.p2}")

            if self.p1 != self.p2:
                winner = "Player 1" if self.p1 > self.p2 else "Player 2"
                print(f"{winner} wins!")
                return winner
