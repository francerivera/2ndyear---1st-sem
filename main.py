import pokemon_selection
import player_random
import player_picking
import battle_simulation


###############

# player_random.py

import random

def dice_roll():
    while True:
        p1, p2 = random.randint(1, 6), random.randint(1, 6)
        print(f"Player 1 rolls: {p1}\nPlayer 2 rolls: {p2}")

        if p1 != p2:
            return "Player 1" if p1 > p2 else "Player 2"

################

# pokemon_selection.py

from tabulate import tabulate

# Pokemon data arrays
pokemon_names = ["Pikachu", "Charizard", "Bulbasaur", "Vaporeon", "Lopunny", "Mewtwo", "Gardevoir", "Lucario", "Gengar", "Snorlax"]
health_points = [100, 120, 105, 110, 100, 115, 125, 110, 100, 105]
power_levels = [100, 110, 70, 90, 60, 90, 100, 110, 80, 80]
poisons = [{"name": "Toxic", "damage": 20}]  # only 1 poison for now
potions = [{"name": "Healing Potion", "heal": 30}]  # only 1 potion for now


def pokemon_table():
    table_data = [
        ["Pokemon"] + pokemon_names[:],  # First row with Pokémon names
        ["Health"] + health_points[:],    # Second row with health values
        ["Power"] + power_levels[:]        # Third row with power values
    ]
    return table_data

print(tabulate(pokemon_table(), tablefmt="grid"))


###############

# player_picking.py

from pokemon_selection import *
from player_random import *

player1_pokemon = []
player2_pokemon = []


def display_table():
    table_data = [
        ["Pokemon"] + pokemon_names[:],
        ["Health"] + health_points[:],
        ["Power"] + power_levels[:]
    ]
    print(tabulate(table_data, tablefmt="grid"))


while True:
    pokemon_count_choice = input("How many Pokemon do you want to fight with? (3 or 4): ")
    if pokemon_count_choice in ['3', '4']:
        pokemon_count = int(pokemon_count_choice)
        break
    else:
        print("Invalid input. Please choose either 3 or 4.")


def get_player_choice(player_name):
    while True:
        print(f"\n{player_name}'s turn:")
        display_table()
        choice = input(f"Select a Pokémon (1-{len(pokemon_names)}): ")
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(pokemon_names):
                return choice_index
            else:
                print("Invalid choice. Please select a valid Pokemon number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


print("Let's roll the dice to determine who is going to pick first!")
first_player = dice_roll()
print(f"{first_player} gets to pick first!")

if first_player == "Player 1":
    for i in range(pokemon_count):
        player1_choice_index = get_player_choice("Player 1")
        player1_pokemon.append(pokemon_names.pop(player1_choice_index))
        health_points.pop(player1_choice_index)
        power_levels.pop(player1_choice_index)

        player2_choice_index = get_player_choice("Player 2")
        player2_pokemon.append(pokemon_names.pop(player2_choice_index))
        health_points.pop(player2_choice_index)
        power_levels.pop(player2_choice_index)
else:
    for i in range(pokemon_count):
        player2_choice_index = get_player_choice("Player 2")
        player2_pokemon.append(pokemon_names.pop(player2_choice_index))
        health_points.pop(player2_choice_index)
        power_levels.pop(player2_choice_index)

        player1_choice_index = get_player_choice("Player 1")
        player1_pokemon.append(pokemon_names.pop(player1_choice_index))
        health_points.pop(player1_choice_index)
        power_levels.pop(player1_choice_index)

# Final selections
print("\nFinal selections:")
print("Player 1:", ', '.join(player1_pokemon))  # Cleanly display Pokémon names
print("Player 2:", ', '.join(player2_pokemon))  # Cleanly display Pokémon names

################

# battle_simulation.py

from pokemon_selection import *
from player_picking import *
import random


def use_item(player_name, player_health, opponent_health, potion_used, poison_used):
    if not potion_used or not poison_used:
        print(f"\n{player_name}, you have a potion and poison to use.")
        if not potion_used:
            print("1. Use Healing Potion (+30 HP)")
        if not poison_used:
            print("2. Use Toxic Poison (-20 opponent HP)")
        print("3. No item")

        choice = input(f"{player_name}, would you like to use any item? (1/2/3): ")
        if choice == '1' and not potion_used:
            player_health += potions[0]["heal"]
            print(f"{player_name} used a Healing Potion! Health is now {player_health:.2f}.")
            potion_used = True
        elif choice == '2' and not poison_used:
            opponent_health -= poisons[0]["damage"]
            print(f"{player_name} used Toxic Poison! Opponent's health is now {opponent_health:.2f}.")
            poison_used = True
        elif choice == '3':
            print(f"{player_name} chose not to use any item.")
        else:
            print("Invalid choice or item already used.")
    return player_health, opponent_health, potion_used, poison_used


def simulate_battle():

    player1_potion_used = False
    player1_poison_used = False
    player2_potion_used = False
    player2_poison_used = False

    print("\nSimulating battles...")


    random.shuffle(player1_pokemon)
    random.shuffle(player2_pokemon)

    for i in range(pokemon_count):
        print(f"\nBattle {i + 1}: {player1_pokemon[i]} vs {player2_pokemon[i]}")


        p1_health = health_points[i]
        p2_health = health_points[i]
        p1_power = power_levels[i]
        p2_power = power_levels[i]


        p1_health, p2_health, player1_potion_used, player1_poison_used = use_item(
            "Player 1", p1_health, p2_health, player1_potion_used, player1_poison_used)


        p2_health, p1_health, player2_potion_used, player2_poison_used = use_item(
            "Player 2", p2_health, p1_health, player2_potion_used, player2_poison_used)


        if p1_power > p2_power:
            print(f"Player 1's {player1_pokemon[i]} wins the battle!")
            p1_health *= 1.05  # Winner's health increases by 5%
            p2_health *= 0.90  # Loser's health decreases by 10%
        elif p2_power > p1_power:
            print(f"Player 2's {player2_pokemon[i]} wins the battle!")
            p2_health *= 1.05  # Winner's health increases by 5%
            p1_health *= 0.90  # Loser's health decreases by 10%
        else:
            print("It's a tie! No health changes applied.")


        p1_health *= 0.98
        p2_health *= 0.98

        print(f"After the battle, Player 1's {player1_pokemon[i]} health: {p1_health:.2f}")
        print(f"After the battle, Player 2's {player2_pokemon[i]} health: {p2_health:.2f}")


simulate_battle()













