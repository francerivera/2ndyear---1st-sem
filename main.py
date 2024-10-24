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

import numpy as np
from tabulate import tabulate

pokemon_data = {
    "Generation 1": [
        ["PIKACHU", "ELECTRIC", 100, 100, "Choice Scarf", 20, "Life Orb", 30],
        ["MEWTWO", "PSYCHIC", 115, 90, "Choice Band", 20, "Leftovers", 30]
    ],
    "Generation 2": [
        ["TYPHLOSION", "FIRE", 120, 110, "Choice Scarf", 20, "Super Potion", 30],
        ["ESPEON", "PSYCHIC", 125, 100, "Life Orb", 20, "Berry", 30]
    ],
    "Generation 3": [
        ["SCEPTILE", "GRASS", 105, 70, "Choice Band", 20, "Super Potion", 30],
        ["BLAZIKEN", "FIRE", 110, 110, "Life Orb", 20, "Leftovers", 30]
    ],
    "Generation 4": [
        ["LUXRAY", "ELECTRIC", 110, 90, "Choice Scarf", 20, "Berry", 30],
        ["LUCARIO", "FIGHTING", 100, 80, "Choice Band", 20, "Super Potion", 30]
    ],
    "Generation 5": [
        ["ZOROARK", "DARK", 100, 60, "Life Orb", 20, "Berry", 30],
        ["SERPERIOR", "GRASS", 105, 80, "Choice Scarf", 20, "Leftovers", 30]
    ]
}

# Create a list to hold the table data
table_data = [["Pokemon", "Type", "Health", "Power", "Poison", "Poison Damage", "Potion", "Potion Heal"]]


for gen, pokemons in pokemon_data.items():
    for pokemon in pokemons:
        table_data.append([gen] + list(pokemon))

# Convert the table data to a NumPy array of type object
pokemon_array = np.array(table_data, dtype=object)


print(tabulate(pokemon_array, headers='firstrow', tablefmt="grid"))


###############

# player_picking.py

from pokemon_selection import *
from player_random import *


def display_pokemon(pokemon_array):
    print(tabulate(pokemon_array[1:], headers=pokemon_array[0], tablefmt="grid"))

def select_pokemon(player, available_pokemon):
    while True:
        try:
            max_choice = len(available_pokemon) - 1
            choice = int(input(f"Player {player}, select a Pokémon (1-{max_choice}): "))
            if 1 <= choice <= max_choice:
                selected = available_pokemon[choice].copy()
                available_pokemon = np.delete(available_pokemon, choice, axis=0)
                # Update the numbering
                available_pokemon[1:, 0] = range(1, len(available_pokemon))
                return selected, available_pokemon
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

# Main game logic
while True:
    pokemon_count_choice = input("How many Pokemon do you want to fight with? (3 or 4): ")
    if pokemon_count_choice in ['3', '4']:
        pokemon_count = int(pokemon_count_choice)
        break
    else:
        print("Invalid input. Please choose either 3 or 4.")

print("Let's roll the dice to determine who is going to pick first!")
first_player = dice_roll()
print(f"{first_player} gets to pick first!")

# Initialize player Pokémon lists
player1_pokemon = []
player2_pokemon = []

# Selection process
for i in range(pokemon_count * 2):
    print("\nAvailable Pokémon:")
    display_pokemon(pokemon_array)

    current_player = 1 if (i % 2 == 0 and first_player == "Player 1") or (i % 2 == 1 and first_player == "Player 2") else 2
    selected_pokemon, pokemon_array = select_pokemon(current_player, pokemon_array)

    if current_player == 1:
        player1_pokemon.append(selected_pokemon)
    else:
        player2_pokemon.append(selected_pokemon)

    print(f"Player {current_player} selected {selected_pokemon[2]}")

# Display final selections
print("\nFinal Selections:")
print("Player 1:")
print(tabulate([pokemon[1:] for pokemon in player1_pokemon], headers=pokemon_array[0][1:], tablefmt="grid"))
print("\nPlayer 2:")
print(tabulate([pokemon[1:] for pokemon in player2_pokemon], headers=pokemon_array[0][1:], tablefmt="grid"))
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













