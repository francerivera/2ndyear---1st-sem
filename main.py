# main.py

import pokemon_selection
import player_random
import player_picking
import battle_simulation
import match_summary


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
    "2000": [
        ["TYPHLOSION", "FIRE", 120, 60],
        ["MEWTWO", "PSYCHIC", 125, 55]
    ],
    "1500": [
        ["PIKACHU", "ELECTRIC", 115, 50],
        ["VAPOREON", "WATER", 115, 55]
    ],
    "1000": [
        ["LUXRAY", "ELECTRIC", 110, 40],
        ["BLAZIKEN", "FIRE", 110, 45]
    ],
    "500": [
        ["SCEPTILE", "GRASS", 105, 35],
        ["GENGAR", "GHOST", 105, 40]
    ],
    "100": [
        ["ZOROARK", "DARK", 100, 30],
        ["LUCARIO", "FIGHTING", 100, 35]
    ]
}

item_data = {
    "Damage Items": {
        "Choice Scarf": {"price": 250, "effect": 20},
        "Choice Band": {"price": 500, "effect": 30},
        "Life Orb": {"price": 1000, "effect": 40}
    },
    "Healing Items": {
        "Berry": {"price": 250, "effect": 20},
        "Super Potion": {"price": 500, "effect": 30},
        "Leftovers": {"price": 1000, "effect": 40}
    }
}

# Create a list to hold the table data for Pokémon
table_data = [["Price", "Pokemon", "Type", "Health", "Power"]]
item_table = [["Category", "Item", "Price", "Effect (Damage/Heal)"]]

# Populate the table data from pokemon_data
for gen, pokemons in pokemon_data.items():
    for pokemon in pokemons:
        table_data.append([gen] + list(pokemon))

for category, items in item_data.items():
    for item, (price, effect) in items.items():
        item_table.append([category, item, price, effect])

pokemon_array = np.array(table_data, dtype=object)

print(tabulate(pokemon_array, headers='firstrow', tablefmt="grid"))

###############

# player_picking.py

from pokemon_selection import *
from player_random import *

# Function to display Pokémon
def display_pokemon(pokemon_array):
    print(tabulate(pokemon_array[1:], headers=pokemon_array[0], tablefmt="grid"))

# Function to display items
def display_items(item_data):
    item_table = [["Category", "Item", "Price", "Effect (Damage/Heal)"]]
    for category, items in item_data.items():
        for item, details in items.items():
            price = details["price"]
            effect = details["effect"]
            item_table.append([category, item, price, effect])
    print(tabulate(item_table, headers="firstrow", tablefmt="grid"))

# Function to select Pokémon
def select_pokemon(player, available_pokemon, balance):
    while True:
        try:
            max_choice = len(available_pokemon) - 1  # Adjust for 1-based user input
            choice = int(input(f"Player {player}, select a Pokemon (1-{max_choice}): "))
            if 1 <= choice <= max_choice:
                selected = available_pokemon[choice].copy()
                price = int(selected[0])  # Get the price of the selected Pokémon

                if price <= balance:
                    balance -= price  # Deduct the price from the balance
                    available_pokemon = np.delete(available_pokemon, choice, axis=0)  # Remove selected Pokémon
                    return selected, available_pokemon, balance  # Return selected Pokémon, remaining Pokémon, and new balance
                else:
                    print("Insufficient funds to buy this Pokémon. Please select another.")
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

# Function to allow item purchase and track purchased items
def purchase_item(player, balance, item_data):
    print(f"\nPlayer {player}, your current balance is: {balance}")
    display_items(item_data)
    purchased_items = []

    while len(purchased_items) < 3:  # Limit to 3 items
        item_choice = input("Select an item to purchase by name (or type 'exit' to skip): ")  # Convert input to lowercase
        if item_choice == 'exit':  # Check if the input is 'exit'
            break

        # Find the item in item_data
        item_found = False
        for category, items in item_data.items():
            if item_choice in items:  # Check against the item names in lowercase
                item_details = items[item_choice]
                price = item_details["price"]
                if price <= balance:
                    balance -= price
                    purchased_items.append((item_choice, category, price, item_details["effect"]))
                    print(f"You purchased {item_choice} for {price} Pokedollars.")
                    print(f"Remaining balance: {balance}")
                else:
                    print("Insufficient funds to buy this item.")
                item_found = True
                break

        if not item_found:
            print("Invalid selection. Please select a valid item name.")

    if len(purchased_items) >= 3:
        print("You have reached the maximum item limit of 3.")

    return balance, purchased_items

# Main game logic
while True:
    pokemon_count_choice = input("How many Pokemon do you want to fight with? (3 or 4): ")
    if pokemon_count_choice in ['3', '4']:
        pokemon_count = int(pokemon_count_choice)
        break
    else:
        print("Invalid input. Please choose either 3 or 4.")

print("Let's roll the dice to determine who is going to pick first!")
first_player = dice_roll()  # Ensure this function is defined
print(f"{first_player} gets to pick first!\n")

# Set initial balances based on the number of Pokémon chosen
if pokemon_count == 3:
    player1_balance = 5000
    player2_balance = 5000
    balance_amount = 5000
else:  # pokemon_count == 4
    player1_balance = 5500
    player2_balance = 5500
    balance_amount = 5500

print(f"Attention Trainers! Both of you will receive {balance_amount} Pokedollars. Use this wisely to prepare for your upcoming battles. Good luck!")

# Initialize player Pokémon lists and balances
player1_pokemon = []
player2_pokemon = []

# Selection process
for i in range(pokemon_count * 2):
    print("\nAvailable Pokemon:")
    display_pokemon(pokemon_array)

    current_player = 1 if (i % 2 == 0 and first_player == "Player 1") or (
            i % 2 == 1 and first_player == "Player 2") else 2
    current_balance = player1_balance if current_player == 1 else player2_balance

    selected_pokemon, pokemon_array, current_balance = select_pokemon(current_player, pokemon_array, current_balance)

    if current_player == 1:
        player1_pokemon.append(selected_pokemon)
        player1_balance = current_balance
    else:
        player2_pokemon.append(selected_pokemon)
        player2_balance = current_balance

    print(f"Player {current_player} selected {selected_pokemon[1]}")
    print(f"Player {current_player}'s remaining balance: {current_balance}")

# Display final selections
print("\nFinal Selections:")
print("Player 1:")
print(tabulate([pokemon[1:] for pokemon in player1_pokemon], headers=["Pokemon", "Type", "Health", "Power"],
               tablefmt="grid"))
print(f"Player 1's final balance: {player1_balance}")
print("\nPlayer 2:")
print(tabulate([pokemon[1:] for pokemon in player2_pokemon], headers=["Pokemon", "Type", "Health", "Power"],
               tablefmt="grid"))
print(f"Player 2's final balance: {player2_balance}")

# Display items and allow each player to make purchases
print("\nItems available for purchase:")
display_items(item_data)

# Player 1 purchases
print("\nPlayer 1, it's time to buy items!")
player1_balance, player1_items = purchase_item(1, player1_balance, item_data)

# Player 2 purchases
print("\nPlayer 2, it's time to buy items!")
player2_balance, player2_items = purchase_item(2, player2_balance, item_data)

# Final balances after item purchase
print(f"\nPlayer 1's final balance: {player1_balance}")
print(f"Player 2's final balance: {player2_balance}")

# Display final loadouts
print("\nFinal Loadouts:")
print("Player 1's Pokémon and Items:")
print(tabulate([pokemon[1:] for pokemon in player1_pokemon], headers=["Pokemon", "Type", "Health", "Power"],
               tablefmt="grid"))
print("Purchased Items:")
print(tabulate(player1_items, headers=["Item", "Category", "Price", "Effect"], tablefmt="grid"))

print("\nPlayer 2's Pokémon and Items:")
print(tabulate([pokemon[1:] for pokemon in player2_pokemon], headers=["Pokemon", "Type", "Health", "Power"],
               tablefmt="grid"))
print("Purchased Items:")
print(tabulate(player2_items, headers=["Item", "Category", "Price", "Effect"], tablefmt="grid"))



################

# battle_simulation.py

import random
from tabulate import tabulate
from match_summary import display_history, log_round
from player_picking import player1_pokemon, player2_pokemon, player1_items, player2_items

# Define type advantages
type_advantages = {
    "FIRE": {"GRASS": 1.5, "WATER": 0.5, "FIRE": 1.0, "ELECTRIC": 1.0, "PSYCHIC": 1.0, "GHOST": 1.0, "DARK": 1.0,
             "FIGHTING": 1.0},
    "PSYCHIC": {"FIGHTING": 1.5, "PSYCHIC": 1.0, "DARK": 0.5, "FIRE": 1.0, "WATER": 1.0, "GRASS": 1.0, "ELECTRIC": 1.0,
                "GHOST": 1.0},
    "ELECTRIC": {"WATER": 1.5, "GRASS": 0.5, "FIRE": 1.0, "ELECTRIC": 1.0, "PSYCHIC": 1.0, "GHOST": 1.0, "DARK": 1.0,
                 "FIGHTING": 1.0},
    "WATER": {"FIRE": 1.5, "GRASS": 0.5, "ELECTRIC": 1.0, "WATER": 1.0, "PSYCHIC": 1.0, "GHOST": 1.0, "DARK": 1.0,
              "FIGHTING": 1.0},
    "GRASS": {"FIRE": 0.5, "WATER": 1.5, "GRASS": 1.0, "ELECTRIC": 1.0, "PSYCHIC": 1.0, "GHOST": 1.0, "DARK": 1.0,
              "FIGHTING": 1.0},
    "GHOST": {"PSYCHIC": 1.5, "GHOST": 1.5, "DARK": 0.5, "FIRE": 1.0, "WATER": 1.0, "GRASS": 1.0, "ELECTRIC": 1.0,
              "FIGHTING": 1.0},
    "DARK": {"PSYCHIC": 1.5, "GHOST": 1.5, "DARK": 1.0, "FIGHTING": 0.5, "FIRE": 1.0, "WATER": 1.0, "GRASS": 1.0,
             "ELECTRIC": 1.0},
    "FIGHTING": {"DARK": 1.5, "PSYCHIC": 0.5, "GHOST": 0.5, "FIGHTING": 1.0, "FIRE": 1.0, "WATER": 1.0, "GRASS": 1.0,
                 "ELECTRIC": 1.0}
}


def display_health_bar(current_health, max_health):
    """Create a health bar representation."""
    bar_length = 20  # Length of the health bar
    health_ratio = current_health / max_health
    filled_length = int(bar_length * health_ratio)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    return f"[{bar}] {current_health}/{max_health}"


def convert_pokemon_to_battle_format(pokemon_list):
    """Convert the pokemon data from player_picking format to battle format."""
    battle_pokemon = []
    for pokemon in pokemon_list:
        battle_pokemon.append({
            "name": pokemon[1],  # Pokemon name
            "health": int(pokemon[3]),  # Health
            "max_health": int(pokemon[3]),  # Max Health
            "power": int(pokemon[4]),  # Power
            "type": pokemon[2]  # Type
        })
    return battle_pokemon


def calculate_damage(attacker, defender):
    """Calculate damage based on power and type advantages."""
    base_damage = attacker['power']

    # Add bonus power from items if it exists
    if 'bonus_power' in attacker:
        base_damage += attacker['bonus_power']

    # Determine effectiveness
    effectiveness = type_advantages.get(attacker['type'], {}).get(defender['type'], 1.0)

    # Calculate final damage
    damage = base_damage * effectiveness

    return damage, effectiveness  # Return both damage and effectiveness


def display_currency(player):
    """Display the currency of a player."""
    return f"{player['name']} Currency: {player['currency']}"


def use_item(player, battle_pokemon, items):
    """Allow the player to use an item on their chosen Pokémon."""
    while True:
        print(f"\n{player}, your current items:")
        print(tabulate(items, headers=["Item", "Category", "Price", "Effect"], tablefmt="grid"))

        print("\nYour Pokémon:")
        for i, pokemon in enumerate(battle_pokemon, 1):
            print(
                f"{i}. {pokemon['name']} - Health: {pokemon['health']}/{pokemon['max_health']} {display_health_bar(pokemon['health'], pokemon['max_health'])}, Power: {pokemon['power']}")
            if 'bonus_power' in pokemon:
                print(f"   Bonus Power: +{pokemon['bonus_power']}")

        # Loop for item name input
        while True:
            item_name = input("Enter the name of the item you want to use (or 'cancel' to skip): ").strip().lower()

            if item_name == 'cancel':
                print("Item use cancelled.")
                return

            # Check if the item exists
            item_found = any(item[0].lower() == item_name for item in items)
            if item_found:
                break  # Exit the loop if a valid item name is entered
            else:
                print("Invalid item name. Please try again.")

        # Loop for Pokémon choice input
        while True:
            pokemon_choice = input(
                "Enter the number of the Pokémon you want to use the item on (or 'cancel' to skip): ").strip()

            if pokemon_choice == 'cancel':
                print("Pokémon selection cancelled.")
                return

            try:
                pokemon_index = int(pokemon_choice) - 1
                if 0 <= pokemon_index < len(battle_pokemon):
                    chosen_pokemon = battle_pokemon[pokemon_index]
                    # Here you can apply the item effect to the chosen Pokémon
                    print(f"You used {item_name} on {chosen_pokemon['name']}.")
                    # Apply item effect logic here (e.g., healing, boosting power, etc.)
                    break  # Exit the loop if a valid Pokémon number is entered
                else:
                    print("Invalid Pokémon number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Find the item and apply its effect
        for item in items:
            if item[0].lower() == item_name:
                effect_value = int(item[3])  # Ensure the effect value is an integer

                if item[1] == "Healing Items":
                    # Healing item
                    new_health = chosen_pokemon['health'] + effect_value
                    chosen_pokemon['health'] = min(chosen_pokemon['max_health'], new_health)
                    print(
                        f"{chosen_pokemon['name']} healed for {effect_value} health! Current health: {chosen_pokemon['health']}/{chosen_pokemon['max_health']} {display_health_bar(chosen_pokemon['health'], chosen_pokemon['max_health'])}")

                elif item[1] in ["Damage Items", "Power"]:
                    # Damage-boosting item
                    if 'bonus_power' not in chosen_pokemon:
                        chosen_pokemon['bonus_power'] = 0
                    chosen_pokemon['bonus_power'] += effect_value
                    print(
                        f"{chosen_pokemon['name']}'s power increased by {effect_value}! Current bonus power: +{chosen_pokemon['bonus_power']}")

                items.remove(item)  # Remove the used item
                return


def battle(pokemon1, pokemon2, player1_currency, player2_currency, round_number, run_command_used, player1_battle_pokemon, player2_battle_pokemon):
    print(f"\nBattle: {pokemon1['name']} ({pokemon1['type']}) vs {pokemon2['name']} ({pokemon2['type']})")
    print(
        f"Health - {pokemon1['name']}: {pokemon1['health']}/{pokemon1['max_health']} {display_health_bar(pokemon1['health'], pokemon1['max_health'])}, "
        f"{pokemon2['name']}: {pokemon2['health']}/{pokemon2['max_health']} {display_health_bar(pokemon2['health'], pokemon2['max_health'])}")

    # Calculate damage and effectiveness
    damage_to_p2, effectiveness1 = calculate_damage(pokemon1, pokemon2)
    damage_to_p1, effectiveness2 = calculate_damage(pokemon2, pokemon1)

    # Apply damage
    pokemon2['health'] = max(0, pokemon2['health'] - damage_to_p2)
    pokemon1['health'] = max(0, pokemon1['health'] - damage_to_p1)

    # Show damage results with effectiveness messages
    if effectiveness1 > 1.0:
        print(f"{pokemon1['name']} deals {damage_to_p2:.1f} damage to {pokemon2['name']} (super effective!)")
    elif effectiveness1 < 1.0:
        print(f"{pokemon1['name']} deals {damage_to_p2:.1f} damage to {pokemon2['name']} (not very effective.)")
    else:
        print(f"{pokemon1['name']} deals {damage_to_p2:.1f} damage to {pokemon2['name']} (no effect.)")

    if effectiveness2 > 1.0:
        print(f"{pokemon2['name']} deals {damage_to_p1:.1f} damage to {pokemon1['name']} (super effective!)")
    elif effectiveness2 < 1.0:
        print(f"{pokemon2['name']} deals {damage_to_p1:.1f} damage to {pokemon1['name']} (not very effective.)")
    else:
        print(f"{pokemon2['name']} deals {damage_to_p1:.1f} damage to {pokemon1['name']} (no effect.)")

    # Determine the winner of the round
    winner = None
    if damage_to_p2 > damage_to_p1:
        print("\nBATTLE RESULT:\n")
        print(f"{pokemon1['name']} wins this round!")
        winner = pokemon1['name']  # Set winner to Player 1's Pokémon name
        # Winner gains health, loser loses health
        pokemon1['health'] = min(pokemon1['max_health'], pokemon1['health'] + 5)
        pokemon2['health'] = max(0, pokemon2['health'] - 10)
        print(f"{pokemon1['name']} gained 5 health points!")
        print(f"{pokemon2['name']} lost 10 health points!")

        # Award currency to player
        player1_currency += 100  # Winner gets more currency
        player2_currency += 50  # Loser gets less currency
    elif damage_to_p1 > damage_to_p2:
        print("\nBATTLE RESULT:\n")
        print(f"{pokemon2['name']} wins this round!")
        winner = pokemon2['name']  # Set winner to Player 2's Pokémon name
        # Winner gains health, loser loses health
        pokemon2['health'] = min(pokemon2['max_health'], pokemon2['health'] + 5)
        pokemon1['health'] = max(0, pokemon1['health'] - 10)
        print(f"{pokemon2['name']} gained 5 health points!")
        print(f"{pokemon1['name']} lost 10 health points!")

        # Award currency to player
        player2_currency += 100  # Winner gets more currency
        player1_currency += 50  # Loser gets less currency
    else:
        print("\nBattle Result:\n")
        print("It's a tie! Both Pokémon dealt equal damage.")
        winner = "Draw"  # Set winner to "Draw" for logging purposes
        player1_currency += 50
        player2_currency += 50

    # Apply fatigue
    fatigue_loss = 2
    pokemon1['health'] = max(0, pokemon1['health'] - fatigue_loss)
    pokemon2['health'] = max(0, pokemon2['health'] - fatigue_loss)
    print(f"Due to fatigue, both Pokémon lost {fatigue_loss} health points.")

    print(
        f"\nAfter fatigue, {pokemon1['name']} health: {pokemon1['health']}/{pokemon1['max_health']} {display_health_bar(pokemon1['health'], pokemon1['max_health'])}")
    print(
        f"After fatigue, {pokemon2['name']} health: {pokemon2['health']}/{pokemon2['max_health']} {display_health_bar(pokemon2['health'], pokemon2['max_health'])}")


    # Check for fainting
    if pokemon1['health'] <= 0 and pokemon2['health'] <= 0:
        print("Both Pokémon fainted!")
        return None, player1_currency, player2_currency, run_command_used
    elif pokemon1['health'] <= 0:
        print(f"{pokemon2['name']} wins!")
        return pokemon2, player1_currency, player2_currency, run_command_used
    elif pokemon2['health'] <= 0:
        print(f"{pokemon1['name']} wins!")
        return pokemon1, player1_currency, player2_currency, run_command_used
    else:
        print("Both Pokémon survive!\n")
        return None, player1_currency, player2_currency, run_command_used

def simulate_battles():
    player1_battle_pokemon = convert_pokemon_to_battle_format(player1_pokemon)
    player2_battle_pokemon = convert_pokemon_to_battle_format(player2_pokemon)

    round_number = 1
    run_command_used = False  # Initialize the run command usage flag

    # Initialize player currency
    player1_currency = 0
    player2_currency = 0

    while player1_battle_pokemon and player2_battle_pokemon:
        print(f"\n=== Round {round_number} ===")
        print("\nCurrent Pokémon Status:")
        print("\nPlayer 1's Pokémon:")
        for pokemon in player1_battle_pokemon:
            print(
                f"{pokemon['name']} - Health: {pokemon['health']}/{pokemon['max_health']} {display_health_bar(pokemon['health'], pokemon['max_health'])}, Power: {pokemon['power']}")

        print("\nPlayer 2's Pokémon:")
        for pokemon in player2_battle_pokemon:
            print(
                f"{pokemon['name']} - Health: {pokemon['health']}/{pokemon['max_health']} {display_health_bar(pokemon['health'], pokemon['max_health'])}, Power: {pokemon['power']}")

        # Battle phase
        input("\nPress Enter to continue to the battle phase...")

        # Randomly select one Pokémon from each player
        p1 = random.choice(player1_battle_pokemon)
        p2 = random.choice(player2_battle_pokemon)

        # Pass round_number, run_command_used, and battle Pokémon lists to the battle function
        winner_info = battle(p1, p2, player1_currency, player2_currency, round_number, run_command_used,
                             player1_battle_pokemon, player2_battle_pokemon)

        if winner_info is None:
            print("No winner determined. Ending the battle.")
            break
        else:
            winner, player1_currency, player2_currency, run_command_used = winner_info

        # Log the round results
        if winner:
            winner_name = winner['name']
        else:
            winner_name = "Draw"

        log_round(round_number, p1, p2, winner_name)  # Log the round results

        # Remove fainted Pokémon
        if p1['health'] <= 0:
            player1_battle_pokemon.remove(p1)
            print(f"{p1['name']} has fainted and is removed from Player 1's team.")
        if p2['health'] <= 0:
            player2_battle_pokemon.remove(p2)
            print(f"{p2['name']} has fainted and is removed from Player 2's team.")

        # Item phase with option to buy the run command
        for player, battle_pokemon, items, currency in [
            ("Player 1", player1_battle_pokemon, player1_items, player1_currency),
            ("Player 2", player2_battle_pokemon, player2_items, player2_currency)
        ]:
            if round_number > 3 and round_number < 8 and not run_command_used and currency >= 200:
                buy_run = input(
                    f"{player}, do you want to buy the run command for 200 currency? (yes/no): ").strip().lower()
                if buy_run == 'yes':
                    currency -= 200
                    run_command_used = True
                    print(f"{player} has used the run command! Ending the game...")

                    # Tally total health
                    total_health_player1 = sum(p['health'] for p in player1_battle_pokemon)
                    total_health_player2 = sum(p['health'] for p in player2_battle_pokemon)

                    print("\nFinal Health Totals:")
                    print(f"Player 1's Total Health: {total_health_player1}")
                    print(f"Player 2's Total Health: {total_health_player2}")

                    display_history()

                    if total_health_player1 > total_health_player2:
                        print("Player 1 wins the match!")
                    else:
                        print("Player 2 wins the match!")
                    return  # End the function to stop further rounds


            view_history = input(f"{player}, do you want to view the match history? (yes/no): ").strip().lower()
            if view_history == 'yes':
                display_history()  # Display the match history

            if battle_pokemon and items:  # Only ask if the player has Pokémon and items left
                print(f"\n{player}, your remaining Pokémon:")
                for pokemon in battle_pokemon:
                    print(f"{pokemon['name']} - Health: {pokemon['health']}/{pokemon['max_health']} {display_health_bar(pokemon['health'], pokemon['max_health'])}")

                item_choice = input(f"{player}, do you want to use an item? (yes/no): ").strip().lower()
                if item_choice == 'yes':
                    use_item(player, battle_pokemon, items)

        # Display currency after each round
        print("\nCurrent Currency Status:")
        print(display_currency({'name': 'Player 1', 'currency': player1_currency}))  # Display currency for Player 1
        print(display_currency({'name': 'Player 2', 'currency': player2_currency}))  # Display currency for Player 2

        round_number += 1
        input("\nPress Enter to continue to the next round...")

    # Determine the winner
    if player1_battle_pokemon:
        print("Match Results")
        print("\nPlayer 1 wins the battle!")
        winner = player1_battle_pokemon
        winning_player = "Player 1"
    else:
        print("Match Result:")
        print("\nPlayer 2 wins the battle!")
        winner = player2_battle_pokemon
        winning_player = "Player 2"

    # Display final statistics
    print(f"\nFinal Battle Statistics:")
    print(f"{winning_player}'s Remaining Pokémon:")
    for pokemon in winner:
        print(
            f"- {pokemon['name']}: Health = {pokemon['health']}/{pokemon['max_health']} {display_health_bar(pokemon['health'], pokemon['max_health'])}, Power = {pokemon['power']}")

    # Display currency earned by each player
    print(f"\nFinal Currency Status:")
    print(f"Player 1's Currency: {player1_currency}")
    print(f"Player 2's Currency: {player2_currency}")

    # Optionally, you can also display the total number of rounds played
    print(f"\nTotal Rounds Played: {round_number - 1}")


# Display initial selections
print("\nInitial Pokémon Selections:")
print("\nPlayer 1's Pokémon:")
print(tabulate([pokemon[1:] for pokemon in player1_pokemon], headers=["Pokémon", "Type", "Health", "Power"],
               tablefmt="grid"))
print("\nPlayer 2's Pokémon:")
print(tabulate([pokemon[1:] for pokemon in player2_pokemon], headers=["Pokémon", "Type", "Health", "Power"],
               tablefmt="grid"))

# Start the battle simulation
input("\nPress Enter to start the battle simulation...")
simulate_battles()


#################

# match_history.py

from tabulate import tabulate

# Global list to store match history
match_history = []

def log_round(round_number, player1_pokemon, player2_pokemon, winner):
    """Log the results of a round."""
    match_history.append({
        "Round": round_number,
        "Player 1 Pokémon": player1_pokemon['name'],
        "Player 1 Health": player1_pokemon['health'],
        "Player 1 Power": player1_pokemon['power'],
        "Player 2 Pokémon": player2_pokemon['name'],
        "Player 2 Health": player2_pokemon['health'],
        "Player 2 Power": player2_pokemon['power'],
        "Winner": winner
    })

def display_history():
    """Display the match history in a tabulated format."""
    if not match_history:
        print("No match history available.")
        return

    print("\nMatch History:")
    print(tabulate(match_history, headers="keys", tablefmt="grid"))

display_history()










