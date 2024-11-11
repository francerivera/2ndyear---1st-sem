import numpy as np
from tabulate import tabulate


class PokemonData:
    def __init__(self):
        self.pokemon_data = {
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

        self.item_data = {
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

    def create_pokemon_table(self):
        table_data = [["Price", "Pokemon", "Type", "Health", "Power"]]
        for gen, pokemons in self.pokemon_data.items():
            for pokemon in pokemons:
                table_data.append([gen] + list(pokemon))
        return np.array(table_data, dtype=object)

    def create_item_table(self):
        item_table = [["Category", "Item", "Price", "Effect (Damage/Heal)"]]
        for category, items in self.item_data.items():
            for item, details in items.items():
                item_table.append([category, item, details["price"], details["effect"]])
        return np.array(item_table, dtype=object)

    def display_pokemon(self):
        pokemon_array = self.create_pokemon_table()
        print(tabulate(pokemon_array, headers='firstrow', tablefmt="grid"))

    def display_items(self):
        item_array = self.create_item_table()
        print(tabulate(item_array, headers='firstrow', tablefmt="grid"))


# Example usage:
game = PokemonData()
print("Available Pokemon:")
game.display_pokemon()
print("\nAvailable Items:")
game.display_items()
