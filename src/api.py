import requests as re
import time
import websocket
import json
import dotenv
import os

dotenv.load_dotenv()

TOKEN_A = os.getenv('BOT_A_TOKEN')
TOKEN_B = os.getenv('BOT_B_TOKEN')

with open("src/data/predefinedMoves/game1.json", "r") as tf:
    predefined_moves = json.load(tf)


# Function to send moves
def make_move(game_id, move, token):

    url = f"https://lichess.org/api/bot/game/{game_id}/move/{move}"
    headers = {"Authorization": f"Bearer {token}"}
    response = re.post(url, headers=headers)
    print(f"Move {move} sent: {response.status_code}")
    return response.status_code


# WebSocket handler for receiving game events
def on_message(ws, message):
    game_event = json.loads(message)
    if 'type' in game_event and game_event['type'] == 'gameFull':
        game_id = game_event['id']
        print(f"Game started! Game ID: {game_id}")

        # Go through the predefined moves
        for index, move in enumerate(predefined_moves):
            current_bot_token = TOKEN_A if index % 2 == 0 else TOKEN_B
            make_move(game_id, move, current_bot_token)
            time.sleep(1)  # Sleep to allow the move to be registered


# Connect to Lichess WebSocket
def connect_to_game(game_id, token):
    url = f"wss://lichess.org/api/bot/game/stream/{game_id}"
    headers = {"Authorization": f"Bearer {token}"}
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                header=[f"Authorization: Bearer {token}"])
    ws.run_forever()


def main():
    # Bot A creates a challenge
    headers_a = {"Authorization": f"Bearer {TOKEN_A}"}
    response = re.post("https://lichess.org/api/challenge/freeMemory2", 
                       headers=headers_a)

    if response.status_code == 200:
        game_id = response.json()['challenge']['id']
        print(f"Challenge created, Game ID: {game_id}")

        # Connect to the game stream and play the predefined moves
        connect_to_game(game_id, TOKEN_A)
    else:
        print(f"Failed to create challenge: {response.status_code}")


if __name__ == "__main__":
    main()
