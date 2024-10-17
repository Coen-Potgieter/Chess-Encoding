import requests as re
import time
import json
import dotenv
import os
from enum import Enum

dotenv.load_dotenv()

TOKEN_A = os.getenv('BOT_A_TOKEN')
TOKEN_B = os.getenv('BOT_B_TOKEN')

A_HEADERS = {"Authorization": f"Bearer {TOKEN_A}"}
B_HEADERS = {"Authorization": f"Bearer {TOKEN_B}"}

API_URL = "https://lichess.org/api"


class EventState(Enum):
    CHALLENGE = 1
    GAME_START = 2
    GAME_FINISH = 3
    GAME_DECLINED = 4


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


def cancel_challenge(bot_headers, game_id):
    response = re.post(f"https://lichess.org/api/challenge/{game_id}/cancel",
                       headers=bot_headers)
    return response


def list_challenges(bot_headers):
    response = re.get(API_URL + "/challenge", headers=bot_headers)
    return response


def make_challenge(bot_headers, target_username):
    response = re.post(
        API_URL + f"/challenge/{target_username}",
        headers=bot_headers,
        json={"color": "white"}
    )
    return response


def get_ongoing_games(bot_headers):
    response = re.get(API_URL + "/account/playing",
                      headers=bot_headers)
    return response


def print_pretty_json(response):
    print(response.status_code)
    print(json.dumps(response.json(), indent=4))


def accept_challenge(bot_headers, game_id):
    response = re.post(API_URL + f"/challenge/{game_id}/accept",
                       headers=bot_headers)
    return response


def listen_to_events(bot_headers):

    with re.get(API_URL + "/stream/event",
                headers=bot_headers, stream=True) as response:

        for line in response.iter_lines():
            if line:
                event = line.decode('utf-8')
                return handle_event(event)
            else:
                print("keep-alive message received")


def handle_event(event):

    event = json.loads(event)
    event_type = event["type"]
    if event_type == "challenge":
        return {"state": EventState.CHALLENGE, "id": event["challenge"]["id"]}
    elif event_type == "gameStart":
        return {"state": EventState.GAME_START, "id": event["game"]["gameId"]}
    elif event_type == "challengeDeclined":
        return {"state": EventState.GAME_DECLINED}
    else:
        return event_type


def clear_all_challenges(bot_headers):

    response = list_challenges(bot_headers)

    if response.status_code == 200:
        resp_json = response.json()

        # cancel all challenges
        if len(resp_json["out"]) >= 1:
            for challenge in resp_json["out"]:
                challenge_id = challenge["id"]
                cancel_response = cancel_challenge(bot_headers, challenge_id)
                if cancel_response.status_code == 200:
                    print(f"Challenge {challenge_id} Successfully Cancelled")
                else:
                    print(f"Error trying to cancel challenge {challenge_id}")

        # decline all challenges
        if len(resp_json["in"]) >= 1:
            for challenge in resp_json["in"]:
                challenge_id = challenge["id"]
                decline_response = decline_challenge(bot_headers, challenge_id)
                if decline_response.status_code == 200:
                    print(f"Challenge {challenge_id} Successfully Declined")
                else:
                    print(f"Error trying to decline challenge {challenge_id}")


def decline_challenge(bot_headers, game_id):
    response = re.post(API_URL + f"/challenge/{game_id}/decline",
                       headers=bot_headers)
    return response


def abort_game(bot_headers, game_id):
    response = re.post(API_URL + f"/bot/game/{game_id}/abort",
                       headers=bot_headers)
    return response


def resign_all_games(bot_headers):
    # get ongoing games
    response = get_ongoing_games(bot_headers)

    if response.status_code == 200:
        resp_json = response.json()

        # loop through all games and abort them
        for game in resp_json["nowPlaying"]:
            game_id = game["gameId"]
            abort_response = abort_game(bot_headers, game_id)
            if abort_response.status_code == 200:
                print(f"Successfully Aborted game {game_id}")
            else:
                print(f"Error trying to abort game {game_id}")


def main():

    pass


if __name__ == "__main__":
    main()
