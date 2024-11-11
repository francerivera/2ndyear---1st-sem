from pokemon_select import PokemonData
from pokemon_random_player import roll_dice
from tabulate import tabulate
import numpy as np


def display_pokemon(pokemon_array):
    print(tabulate(pokemon_array[1:], headers=pokemon_array[0], tablefmt="grid"))


def display_items(item_data):
    item_table = [["Category", "Item", "Price", "Effect (Damage/Heal)"]]
    for category, items in item_data.items():
        for item, details in items.items():
            price = details["price"]
            effect = details["effect"]
            item_table.append([category, item, price, effect])
    print(tabulate(item_table, headers="firstrow", tablefmt="grid"))


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


class PokemonGame:
    def __init__(self):
        self.player1_balance = 0
        self.player2_balance = 0
        self.player1_pokemon = []
        self.player2_pokemon = []

        # Initialize Pokémon and item data using PokemonData class
        self.pokemon_data = PokemonData()
        self.pokemon_array = self.pokemon_data.create_pokemon_table()
        self.item_data = self.pokemon_data.item_data

    def purchase_item(self, player, balance):
        print(f"\nPlayer {player}, your current balance is: {balance}")
        display_items(self.item_data)
        purchased_items = []

        while len(purchased_items) < 3:  # Limit to 3 items
            item_choice = input("Select an item to purchase by name (Ex: Leftovers) or 'exit' to skip): ").strip()
            if item_choice.lower() == 'exit':
                break

            # Find the item in item_data (case-insensitive match)
            item_found = False
            for category, items in self.item_data.items():
                for item in items:
                    if item_choice.lower() == item.lower():  # Case-insensitive comparison
                        item_details = items[item]
                        price = item_details["price"]
                        if price <= balance:
                            balance -= price
                            purchased_items.append((item, category, price, item_details["effect"]))
                            print(f"You purchased {item} for {price} Pokedollars.")
                            print(f"Remaining balance: {balance}")
                        else:
                            print("Insufficient funds to buy this item.")
                        item_found = True
                        break
                if item_found:
                    break

            if not item_found:
                print("Invalid selection. Please select a valid item name.")

        if len(purchased_items) >= 3:
            print("You have reached the maximum item limit of 3.")

        return balance, purchased_items

    def start_game(self):
        while True:
            pokemon_count_choice = input("How many Pokemon do you want to fight with? (3 or 4): ")
            if pokemon_count_choice in ['3', '4']:
                pokemon_count = int(pokemon_count_choice)
                break
            else:
                print("Invalid input. Please choose either 3 or 4.")

        print("Let's roll the dice to determine who is going to pick first!")
        first_player = roll_dice()  # Ensure this function is defined
        print(f"{first_player} gets to pick first!\n")

        # Set initial balances based on the number of Pokémon chosen
        if pokemon_count == 3:
            self.player1_balance = 5000
            self.player2_balance = 5000
        else:  # pokemon_count == 4
            self.player1_balance = 5500
            self.player2_balance = 5500

        print(
            f"Attention Trainers! Both of you will receive {self.player1_balance} Pokedollars. Use this wisely to prepare for your upcoming battles. Good luck!")

        # Selection process
        for i in range(pokemon_count * 2):
            print("\nAvailable Pokemon:")
            display_pokemon(self.pokemon_array)

            current_player = 1 if (i % 2 == 0 and first_player == "Player 1") or (
                    i % 2 == 1 and first_player == "Player 2") else 2
            current_balance = self.player1_balance if current_player == 1 else self.player2_balance

            selected_pokemon, self.pokemon_array, current_balance = select_pokemon(current_player, self.pokemon_array, current_balance)

            if current_player == 1:
                self.player1_pokemon.append(selected_pokemon)
                self.player1_balance = current_balance
            else:
                self.player2_pokemon.append(selected_pokemon)
                self.player2_balance = current_balance

            print(f"Player {current_player} selected {selected_pokemon[1]}")
            print(f"Player {current_player}'s remaining balance: {current_balance}")

        # Display final selections
        print("\nFinal Selections:")
        print("Player 1:")
        print(tabulate([pokemon[1:] for pokemon in self.player1_pokemon], headers=["Pokemon", "Type", "Health", "Power"], tablefmt="grid"))
        print(f"Player 1's final balance: {self.player1_balance}")
        print("\nPlayer 2:")
        print(tabulate([pokemon[1:] for pokemon in self.player2_pokemon], headers=["Pokemon", "Type", "Health", "Power"], tablefmt="grid"))
        print(f"Player 2's final balance: {self.player2_balance}")

        # Display items and allow each player to make purchases
        print("\nItems available for purchase:")
        display_items(self.item_data)

        # Player 1 purchases
        print("\nPlayer 1, it's time to buy items!")
        self.player1_balance, player1_items = self.purchase_item(1, self.player1_balance)

        # Player 2 purchases
        print("\nPlayer 2, it's time to buy items!")
        self.player2_balance, player2_items = self.purchase_item(2, self.player2_balance)

        # Final balances after item purchase
        print(f"\nPlayer 1's final balance: {self.player1_balance}")
        print(f"Player 2's final balance: {self.player2_balance}")

        # Display final loadouts
        print("\nFinal Loadouts:")
        print("Player 1's Pokémon and Items:")
        print(tabulate([pokemon[1:] for pokemon in self.player1_pokemon], headers=["Pokemon", "Type", "Health", "Power"], tablefmt="grid"))
        print("Purchased Items:")
        print(tabulate(player1_items, headers=["Item", "Category", "Price", "Effect"], tablefmt="grid"))

        print("\nPlayer 2's Pokémon and Items:")
        print(tabulate([pokemon[1:] for pokemon in self.player2_pokemon], headers=["Pokemon", "Type", "Health", "Power"], tablefmt="grid"))
        print("Purchased Items:")
        print(tabulate(player2_items, headers=["Item", "Category", "Price", "Effect"], tablefmt="grid"))


# Run the game
game = PokemonGame()
