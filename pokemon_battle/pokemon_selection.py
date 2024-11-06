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