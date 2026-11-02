import json
import logging
import os
import requests

if not os.path.exists("logs/lab4.log"):
    print("Log file does not exist. Please run tell_me_a_joke.py first to create the log file.")
    exit(1)

logging.basicConfig(
    filename="logs/lab4.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def convert_rank(cardval):
    map = {'JACK': 11, 'QUEEN': 12, 'KING': 13, 'ACE': 14}
    if cardval in map:
        return map[cardval]
    try:
        return int(cardval)
    except ValueError:
        return 0

def summarize(winner, round_num, round_history):
    summary = f"Final Winner: {winner}\nTotal Rounds: {round_num}\n"
    with open("data/high_card_result.txt", "w") as f:
        f.write(summary)
    with open("data/high_card_rounds.json", "w") as f:
        json.dump(round_history, f, indent=4)
    logging.info("[LAB4_GAME_END]")
    print(f"Game Over! {winner} won after {round_num} round(s).")

def draw_card(active_players, draw_data, round_num, round_history):
    round_results = {}
    max_val = -1

    for index, player in enumerate(active_players):
        card = draw_data['cards'][index]
        val = convert_rank(card['value'])
        round_results[player] = {'card': f"{card['value']} of {card['suit']}", 'value': val}
        if val > max_val:
            max_val = val
                
    top = [p for p, data in round_results.items() if data['value'] == max_val]
                
    round_history.append({
        "round": round_num,
        "results": round_results,
        "top_players": top
    })
    return top

def main():
    try:
        deck_resp = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1', timeout=10)
        deck_data = deck_resp.json()
        deck_id = deck_data['deck_id']
        logging.info("[LAB4_DECK_CREATE_OK]")
        
        if deck_resp.status_code == 200:
            try:
                num_players = int(input("Enter number of players (2-40): ")) # tested up to 45
                if num_players < 2 or num_players > 40:
                    raise ValueError
            except ValueError:
                print("Invalid player count.")
                return

            round_num = 1
            players_total = [f"Player {i+1}" for i in range(num_players)]
            players_in = players_total.copy()
            round_history = []
            winner = None

            while not winner:
                draw_resp = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={len(players_in)}', timeout=10)
                draw_data = draw_resp.json()
                logging.info("[LAB4_DRAW_OK]")
                
                top = draw_card(players_in, draw_data, round_num, round_history)
            
                if len(top) == 1:
                    winner = top[0]
                else:
                    logging.info("[LAB4_TIE_ROUND]")
                    players_in = top
                    print(f"Round {round_num} resulted in a tie between: {', '.join(top)}. Proceeding to next round.")
                    round_num += 1

            summarize(winner, round_num, round_history)

    except requests.RequestException:
        logging.error("[LAB4_ERR] Network error during the game.")
        print("A network error occurred during the game.")

    except IndexError:
        logging.error("[LAB4_ERR] Not enough cards to draw.")
        print("Not enough cards to draw. The game cannot continue.")

if __name__ == "__main__":
    main()
    logging.info("[LAB4_END]")