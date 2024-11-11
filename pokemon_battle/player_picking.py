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
        item_choice = input(
            "Select an item to purchase by name (ex: Super Potion) or 'exit'): ")  # Convert input to lowercase
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

print(
    f"Attention Trainers! Both of you will receive {balance_amount} Pokedollars. Use this wisely to prepare for your upcoming battles. Good luck!")

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
