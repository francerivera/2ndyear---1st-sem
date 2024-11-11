import random
from tabulate import tabulate
from pokemon_match_summary import display_history, log_round
from pokemon_player_pick import PokemonGame

# player1_pokemon, player2_pokemon, player1_items, player2_items)

poke = PokemonGame()
player1_pokemon = poke.player1_pokemon
player2_pokemon = poke.player2_pokemon
player1_items = poke.player1_items
player2_items = poke.player2_items

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


def use_item(player, battle_pokemon, items, currency):
    """Allow the player to use an item on their chosen Pokémon and update currency."""
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
                return currency

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
                return currency

            try:
                pokemon_index = int(pokemon_choice) - 1
                if 0 <= pokemon_index < len(battle_pokemon):
                    chosen_pokemon = battle_pokemon[pokemon_index]
                    print(f"You used {item_name} on {chosen_pokemon['name']}.")
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
                return currency


def battle(pokemon1, pokemon2, player1_currency, player2_currency, round_number, run_command_used, player1_wins,
           player2_wins):
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
    winning_player = None  # To keep track of which player won
    if damage_to_p2 > damage_to_p1:
        print("\nBATTLE RESULT:\n")
        print(f"{pokemon1['name']} wins this round!")
        winner = pokemon1['name']  # Set winner to Player 1's Pokémon name
        winning_player = "Player 1"  # Track the winning player

        # Winner gains health, loser loses health
        pokemon1['health'] = min(pokemon1['max_health'], pokemon1['health'] + 5)
        pokemon2['health'] = max(0, pokemon2['health'] - 10)
        print(f"{pokemon1['name']} gained 5 health points!")
        print(f"{pokemon2['name']} lost 10 health points!")

        player1_wins += 1
        # Award currency to players
        player1_currency += 100  # Winner gets more currency
        player2_currency += 50  # Loser gets currency

    elif damage_to_p1 > damage_to_p2:
        print("\nBATTLE RESULT:\n")
        print(f"{pokemon2['name']} wins this round!")
        winner = pokemon2['name']  # Set winner to Player 2's Pokémon name
        winning_player = "Player 2"

        # Winner gains health, loser loses health
        pokemon2['health'] = min(pokemon2['max_health'], pokemon2['health'] + 5)
        pokemon1['health'] = max(0, pokemon1['health'] - 10)
        print(f"{pokemon2['name']} gained 5 health points!")
        print(f"{pokemon1['name']} lost 10 health points!")

        player2_wins += 1
        # Award currency to players
        player2_currency += 100  # Winner gets more currency
        player1_currency += 50  # Loser gets currency

    else:
        print("\nBattle Result:\n")
        print("It's a tie! Both Pokémon dealt equal damage.")
        winner = "Draw"  # Set winner to "Draw" for logging purposes
        player1_currency += 50  # Both players get currency in case of a tie
        player2_currency += 50

    log_round(round_number, pokemon1, pokemon2, winner)

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
        winner = "Draw"
    elif pokemon1['health'] <= 0:
        print(f"{pokemon2['name']} wins!")
        winner = pokemon2['name']
    elif pokemon2['health'] <= 0:
        print(f"{pokemon1['name']} wins!")
        winner = pokemon1['name']
    else:
        print("Both Pokémon survive!\n")
        winner = "None"  # No winner if both are still alive

    return winner, player1_currency, player2_currency, run_command_used, winning_player, player1_wins, player2_wins


def simulate_battles():
    player1_battle_pokemon = convert_pokemon_to_battle_format(player1_pokemon)
    player2_battle_pokemon = convert_pokemon_to_battle_format(player2_pokemon)

    round_number = 0  # Start from 0
    run_command_used = False  # Initialize the run command usage flag

    # Initialize player currency
    player1_currency = 0
    player2_currency = 0

    player1_wins = 0
    player2_wins = 0

    match_history = []  # List to track match history

    while player1_battle_pokemon and player2_battle_pokemon:
        round_number += 1  # Increment round number at the start of the loop
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
        winner_info = battle(p1, p2, player1_currency, player2_currency, round_number, run_command_used, player1_wins, player2_wins)

        # Unpack all returned values
        winner, player1_currency, player2_currency, run_command_used, winning_player, player1_wins, player2_wins = winner_info

        if winner_info is None:
            print("No winner determined. Ending the battle.")
            break


        # Remove fainted Pokémon
        if p1['health'] <= 0:
            player1_battle_pokemon.remove(p1)
            print(f"{p1['name']} has fainted and is removed from Player 1's team.")
        if p2['health'] <= 0:
            player2_battle_pokemon.remove(p2)
            print(f"{p2['name']} has fainted and is removed from Player 2's team.")

        # Item phase: Ask players if they want to use an item
        for player, battle_pokemon, items, currency_var in [
            ("Player 1", player1_battle_pokemon, player1_items, "player1_currency"),
            ("Player 2", player2_battle_pokemon, player2_items, "player2_currency")
        ]:
            if 3 < round_number < 8 and not run_command_used and locals()[currency_var] >= 200:
                buy_run = input(
                    f"\n{player}, Do you want to buy the run command for 200 currency? (yes/no): ").strip().lower()
                if buy_run == 'yes':
                    locals()[currency_var] = max(0, locals()[currency_var] - 200)
                    run_command_used = True
                    print(f"{player} has used the run command! Ending the game...")
                    # Display final statistics immediately after using the run command
                    display_final_statistics(player1_battle_pokemon, player2_battle_pokemon, player1_currency,
                                             player2_currency, round_number, player1_wins, player2_wins)
                    return  # End the function to stop further rounds

            if battle_pokemon and items:  # Only ask if the player has Pokémon and items left
                print(f"\n{player}, your remaining Pokémon:")
                for pokemon in battle_pokemon:
                    print(
                        f"{pokemon['name']} - Health: {pokemon['health']}/{pokemon['max_health']} {display_health_bar(pokemon['health'], pokemon['max_health'])}")

                item_choice = input(f"{player}, do you want to use an item? (yes/no): ").strip().lower()
                if item_choice == 'yes':
                    # Call the use_item function and update currency
                    if player == "Player 1":
                        player1_currency = use_item(player, battle_pokemon, items, player1_currency)
                    else:
                        player2_currency = use_item(player, battle_pokemon, items, player2_currency)

        # Automatically display match history after every 3 rounds
        if round_number % 3 == 0:
            print("\n=== Match History ===")
            for entry in match_history:
                print(f"Round {entry['round']}: {entry['player1_pokemon']} vs {entry['player2_pokemon']} - Winner: {entry['winner']}")

        # Display currency after each round
        print("\nCurrent Currency Status:")
        print(display_currency({'name': 'Player 1', 'currency': player1_currency}))  # Display currency for Player 1
        print(display_currency({'name': 'Player 2', 'currency': player2_currency}))  # Display currency for Player 2

    # Determine the winner if the game ends naturally
    if player1_battle_pokemon:
        print("\nMatch Results")
        print("\nPlayer 1 wins the battle!")
    else:
        print("\nMatch Result:")
        print("\nPlayer 2 wins the battle!")

    # Display final statistics
    display_final_statistics(player1_battle_pokemon, player2_battle_pokemon, player1_currency, player2_currency,
                             round_number, player1_wins, player2_wins)


def display_final_statistics(player1_battle_pokemon, player2_battle_pokemon, player1_currency, player2_currency,
                             player1_wins, player2_wins, round_number):
    display_history()
    print(f"\nFinal Battle Statistics:")
    print("\nPlayer 1's Remaining Pokémon:")
    if player1_battle_pokemon:
        for pokemon in player1_battle_pokemon:
            print(f"- {pokemon['name']}: Health = {pokemon['health']}/{pokemon['max_health']} {display_health_bar(pokemon['health'], pokemon['max_health'])}, Power = {pokemon['power']}")
    else:
        print("No remaining Pokémon.")

    # Display remaining Pokémon for Player 2
    print("\nPlayer 2's Remaining Pokémon:")
    if player2_battle_pokemon:
        for pokemon in player2_battle_pokemon:
            print(f"- {pokemon['name']}: Health = {pokemon['health']}/{pokemon['max_health']} {display_health_bar(pokemon['health'], pokemon['max_health'])}, Power = {pokemon['power']}")
    else:
        print("No remaining Pokémon.")

    # Tally total health for both players
    total_health_player1 = sum(p['health'] for p in player1_battle_pokemon)
    total_health_player2 = sum(p['health'] for p in player2_battle_pokemon)

    print("\nFinal Health Totals:")
    print(f"Player 1's Total Health: {total_health_player1}")
    print(f"Player 2's Total Health: {total_health_player2}")

    print(f"\nFinal Currency Status:")
    print(f"Player 1's Currency: {player1_currency}")
    print(f"Player 2's Currency: {player2_currency}")

    print(f"\nTotal Rounds Won:")
    print(f"Player 1: {player1_wins} rounds")
    print(f"Player 2: {player2_wins} rounds")

    print(f"\nTotal Rounds Played: {round_number}")
    if total_health_player1 > total_health_player2:
        print("Player 1 wins the match!")
    elif player2_wins > player1_wins:
        print("Player 2 wins the match!")
    else:
        print("The match is a draw!")


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
