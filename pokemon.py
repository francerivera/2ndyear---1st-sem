import random

# Dictionary holding Pokemon names, types, and base power
pokemon_dict = {
    "PIKACHU": ("ELECTRIC", 50),
    "CHARMANDER": ("FIRE", 55),
    "BULBASAUR": ("GRASS", 60),
    "SQUIRTLE": ("WATER", 58),
    "JIGGLYPUFF": ("FAIRY", 45),
    "EEVEE": ("NORMAL", 52),
    "SNORLAX": ("NORMAL", 80),
    "GENGAR": ("POISON", 70),
    "MACHAMP": ("FIGHTING", 75),
    "MEWTWO": ("PSYCHIC", 90),
    "DIGLETT": ("GROUND", 55),
    "MAGNEMITE": ("STEEL", 35),
    "ONIX": ("ROCK", 45),
    "GIRATINA": ("GHOST", 90),
    "ARCANINE": ("FIRE", 45),
}

# Game introduction and menu options
print("Welcome to my Pokemon Game!")
print("a.) Play\nb.) Tutorial")

while True:
    user_input = input("Enter 'a' to play or 'b' for the tutorial: ")
    # Displaying the list of available Pokemon and their base power
    if user_input == "a":
        print("┌" + "─" * 14 + "┬" + "─" * 12 + "┬" + "─" * 11 + "┐")
        print("│ Pokemons     │ Types      │ Base Power│")
        print("├" + "─" * 14 + "┼" + "─" * 12 + "┼" + "─" * 11 + "┤")

        for pokemon, (element, power) in sorted(pokemon_dict.items()):
            print(f"│ {pokemon:12} │ {element:10} │ {power:3}       │")

        print("└" + "─" * 14 + "┴" + "─" * 12 + "┴" + "─" * 11 + "┘")
        break
    elif user_input == "b":
        # Tutorial explaining the game mechanics
        print("""To start playing this game:\n
1. Choose your starter Pokemon from the available options. Each has unique types.
2. Pay attention to type advantages, such as strong water against Fire.
3. If you have a strong element versus your opponent, you will have an additional power. If you have a weak element versus your opponent, the additional power will be given to the opponent. If they are the same element, it can be a tie.
4. Your opponent will be random so it is all luck. Good luck!
5. There are keys to help you navigate inside the game. Enter the keys that you want.
6. "Gotta catch 'em all!"\n""")
    else:
        print("Invalid input. Please enter 'a' to play or 'b' for the tutorial.")

# Interactions between elements, first list contains elements strong against the index
# the second list contains elements weak against it
elements_interact = [
    [["GRASS", "STEEL"], ["WATER", "ROCK", "FIRE"]],  # FIRE
    [["WATER"], ["GROUND"]],  # ELECTRIC
    [["WATER", "GROUND", "ROCK"], ["FIRE", "POISON"]],  # GRASS
    [["FIRE", "GROUND", "ROCK"], ["ELECTRIC", "GRASS"]],  # WATER
    [["FIGHTING", "POISON"], ["GHOST"]],  # PSYCHIC
    [["NORMAL", "ROCK", "STEEL"], ["PSYCHIC", "FAIRY"]],  # FIGHTING
    [["FIRE", "ELECTRIC", "POISON", "ROCK", "STEEL"], ["WATER", "GRASS"]],  # GROUND
    [["FIRE"], ["WATER", "GRASS", "FIGHTING", "GROUND", "STEEL"]],  # ROCK
    [["PSYCHIC", "GHOST"], ["GHOST", "DARK"]],  # GHOST
    [["ICE", "ROCK", "FAIRY"], ["FIRE", "FIGHTING", "GROUND"]],  # STEEL
    [["FIGHTING", "DRAGON", "DARK"], ["POISON", "STEEL"]],  # FAIRY
    [[], ["ROCK", "STEEL", "GHOST"]],  # NORMAL
    [["GRASS", "FAIRY"], ["GROUND", "PSYCHIC"]]  # POISON
]

# Mapping element names to their indices in the `elements_interact` list
element_indices = {
    "FIRE": 0,
    "ELECTRIC": 1,
    "GRASS": 2,
    "WATER": 3,
    "PSYCHIC": 4,
    "FIGHTING": 5,
    "GROUND": 6,
    "ROCK": 7,
    "GHOST": 8,
    "STEEL": 9,
    "FAIRY": 10,
    "NORMAL": 11,
    "POISON": 12
}

# Initialize variables for storing match history and tracking match numbers
match_history = []
match_number = 1

# Variables for storing player's Pokemon choice and its power
player_pokemon = ""
player_power = 0

# Main loop for selecting a Pokémon and battling
while True:
    pokemon_input = str(input("Please select a Pokemon: ")).upper()

    if pokemon_input in pokemon_dict:
        # Randomly select a Pokémon for the computer opponent
        computer_choice = random.choice(list(pokemon_dict.keys()))


        def assign_elements(player_pokemon, computer_pokemon):
            global match_number
            player_element, player_power = pokemon_dict[player_pokemon]
            computer_element, computer_power = pokemon_dict[computer_pokemon]

            print(f"Player's {player_pokemon} Element: {player_element}, Power: {player_power}")
            print(f"Computer's {computer_pokemon} Element: {computer_element}, Power: {computer_power}")

            # When both Pokemon have the same element
            if player_element == computer_element:
                random_number = random.randint(1, 10)
                damage = player_power + random_number
                damage2 = computer_power + random_number
                print(
                    f"Both Pokémon have the same element!\nYour Pokémon gained a random additional power: {damage}\nComputer's Pokémon gained a random additional power: {damage2}")
            # When player's Pokemon is strong against the computer's Pokemon
            elif computer_element in elements_interact[element_indices[player_element]][0]:
                damage = player_power * 2
                damage2 = computer_power
                print(f"{player_element} is strong against {computer_element}! Damage is 2x: {damage}")
            # when player's Pokemon is weak against the computer's Pokemon
            elif computer_element in elements_interact[element_indices[player_element]][1]:
                damage = player_power * 0.5
                damage2 = computer_power
                print(f"{player_element} is weak against {computer_element}! Damage is 1/2: {damage}")
            # When there is no special effect between the Pokemon types
            else:
                damage = player_power
                damage2 = computer_power
                print(f"{player_element} has no special effect on {computer_element}. Damage is: {damage}")

            # Determine the winner based on damage values
            if damage > damage2:
                print(
                    f"Player wins! Your {player_pokemon} will absorb Computer's {computer_pokemon} power. New Power: {damage + damage2}")
                after_battle_player_power = damage + damage2
                after_battle_computer_power = 0
                match_result = "Player wins"
            elif damage < damage2:
                print(
                    f"Computer wins! Computer's {computer_pokemon} will absorb your {player_pokemon}'s power. New Power: {damage2 + damage}")
                after_battle_player_power = 0
                after_battle_computer_power = damage2 + damage
                match_result = "Computer wins"
            else:
                print("It's a tie!")
                after_battle_player_power = player_power
                after_battle_computer_power = computer_power
                match_result = "Tie"

            # Add match result to history
            match_history.append({
                "Match Number": match_number,
                "Player Pokémon": player_pokemon,
                "Player Power (before)": player_power,
                "Player Additional Damage": damage - player_power,
                "Player Total Damage": damage,
                "Computer Pokémon": computer_pokemon,
                "Computer Power (before)": computer_power,
                "Computer Additional Damage": damage2 - computer_power,
                "Computer Total Damage": damage2,
                "Match Result": match_result,
                "Player Power (after)": after_battle_player_power,
                "Computer Power (after)": after_battle_computer_power
            })

            # Increment match number for the next battle
            match_number += 1
            return match_result


        # Execute battle and get the match result
        match_result = assign_elements(pokemon_input, computer_choice)
    else:
        print("Invalid Pokémon selected. Please try again.")
        continue

    # Save progress for the player
    saved_progress = {
        "player_pokemon": None,
        "player_power": 0
    }

    player_progress = 0

    # Ask if the player wants to continue playing or select other options in the menu
    while True:
        print("\nDo you want to continue fighting enemies?")
        print(
            "Enter the key from the choices:\n'n' : New Pokemon\n'm' : Match History\n'x' : Exit")
        if match_result == "Player wins":
            print("\n'c' : Continue")
        user_select = input("Enter the key: ")


        if user_select.lower() == 'm':
            print("{:<15} {:<15} {:<20} {:<25} {:<20} {:<25} {:<25} {:<20} {:<20} {:<20}".format(
                "Match Number", "Player Pokémon", "Player Power (before)", "Player Additional Damage",
                "Player Total Damage", "Computer Power (before)", "Computer Additional Damage",
                "Computer Total Damage", "Match Result", "Player Power (after)", "Computer Power (after)"
            ))
            for match in match_history:
                print("{:<15} {:<15} {:<20} {:<25} {:<20} {:<25} {:<25} {:<20} {:<20} {:<20}".format(
                    match["Match Number"], match["Player Pokémon"], match["Player Power (before)"],
                    match["Player Additional Damage"], match["Player Total Damage"],
                    match["Computer Power (before)"], match["Computer Additional Damage"],
                    match["Computer Total Damage"], match["Match Result"],
                    match["Player Power (after)"], match["Computer Power (after)"]
                ))

            # Summarize the results
            total_matches = len(match_history)
            player_wins = sum(1 for match in match_history if match["Match Result"] == "Player wins")
            computer_wins = sum(1 for match in match_history if match["Match Result"] == "Computer wins")
            ties = sum(1 for match in match_history if match["Match Result"] == "Tie")

            print("\nSummary:")
            print(f"Total Matches: {total_matches}")
            print(f"Player Wins: {player_wins}")
            print(f"Computer Wins: {computer_wins}")
            print(f"Ties: {ties}")

            input("Enter any key to go back: ")
            continue

        elif user_select.lower() == "c":
            if match_result == "Player wins":
                # Continue playing with the winning Pokémon
                previous_power = match_history[-1]["Player Power (after)"]  # Get the previous power
                computer_choice = random.choice(list(pokemon_dict.keys()))
                computer_power = pokemon_dict[computer_choice][1]  # Get the computer's power

                # Increase player's Pokémon power
                pokemon_dict[pokemon_input] = (
                    pokemon_dict[pokemon_input][0],
                    previous_power + pokemon_dict[pokemon_input][1]  # Add the previous power to the current power
                )

                # Determine consecutive wins
                consecutive_wins = sum(1 for match in match_history[-3:] if match.get("Result") == "Player wins")

                # Add a random factor to the computer's power, scaled by consecutive wins
                random_factor = random.uniform(1, 1.5)  # Reduce the randomness range

                # Ensure the computer's power increases gradually
                pokemon_dict[computer_choice] = (
                    pokemon_dict[computer_choice][0],
                    computer_power + int(pokemon_dict[pokemon_input][1] * random_factor)
                )

                match_result = assign_elements(pokemon_input, computer_choice)
                continue
            else:
                print("Invalid Input")
                continue

        # When the user wants to change the pokemon
        elif user_select.lower() == "n":
            if match_result == "Player wins":
                print("Your progress will lose if you proceed")
                print("'e' : No, I changed my mind\n'y' : Yes")
                change_choice = input("Enter the key: ")
                if change_choice.lower() == "e":
                    continue
                elif change_choice.lower() == "y":
                    computer_pokemon = ""
                    computer_power = 0

            selected_pokemon = ""
            selected_pokemon_power = 0
            break

        # When the user wants to quit
        elif user_select.lower() == "x":
            while True:
                print("Do you want to quit? All progress will be lost")
                print("'e' : No, I changed my mind\n'y' : Yes")
                exit_input = input("Enter the key: ")
                if exit_input.lower() == 'y':
                    print("Thank you for playing!")
                    quit()
                elif exit_input.lower() == 'e':
                    break
                else:
                    print("Invalid Input")
                    continue

        else:
            print("Invalid input")
            continue


# need summary in match history
