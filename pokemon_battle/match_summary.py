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