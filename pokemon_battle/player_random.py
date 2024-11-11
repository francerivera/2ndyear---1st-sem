import random

def dice_roll():
    while True:
        p1, p2 = random.randint(1, 6), random.randint(1, 6)
        print(f"Player 1 rolls: {p1}\nPlayer 2 rolls: {p2}")

        if p1 != p2:
            return "Player 1" if p1 > p2 else "Player 2"
