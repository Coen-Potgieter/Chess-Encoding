import requests as re
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


class GameState(Enum):
    GAME_FULL = 1
    GAME_STATE = 2


class Colour(Enum):
    WHITE = 1
    BLACK = 2


def load_moves(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


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
        return {"state": EventState.GAME_START, "id": event["game"]["gameId"],
                "my_turn": event["game"]["isMyTurn"]}
    elif event_type == "challengeDeclined":
        return {"state": EventState.GAME_DECLINED}
    elif event_type == "gameFinish":
        return {"state": EventState.GAME_FINISH}
    else:
        # To log unexpected behaviour
        print(event_type)
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


def resign_game(bot_headers, game_id):
    response = re.post(API_URL + f"/bot/game/{game_id}/resign",
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
            abort_response = resign_game(bot_headers, game_id)
            if abort_response.status_code == 200:
                print(f"Successfully resigned game {game_id}")
            else:
                print(f"Error trying to resign game {game_id}")


def whose_turn(moves):
    moves = moves.split(" ")
    num_moves_played = len(moves)

    # if the number of moves played is divisible by 2 then its whites turn
    if num_moves_played % 2 == 0:
        return Colour.WHITE
    else:
        return Colour.BLACK


def draw_accept_or_make_offer(bot_headers, game_id):

    # this endpoint is used for both offering a draw or accepting a draw
    response = re.post(API_URL + f"/bot/game/{game_id}/draw/yes",
                       headers=bot_headers)
    return response


def play_game(bot_headers, game_id, moves, colour):

    num_moves = len(moves)
    move_idx = 0
    with re.get(API_URL + f"/bot/game/stream/{game_id}",
                headers=bot_headers, stream=True) as response:

        for line in response.iter_lines():
            if line:
                game_event = line.decode('utf-8')
                game_event = json.loads(game_event)
                game_state = game_event["type"]
                if game_state == "gameFull":
                    print("Game has started, White to play")

                    # Game has just begun and white must make the first move
                    if colour == Colour.WHITE:

                        move_to_play = moves[move_idx]
                        move_resp = make_move(bot_headers, game_id,
                                              move_to_play)
                        if move_resp.status_code == 200:
                            print(f"I played {move_to_play} Successfully\n")
                            move_idx += 1
                        else:
                            print(f"Error playing {move_to_play}\n")
                elif game_state == "gameState":
                    if game_event["status"] == "mate":
                        print(f"{game_event["winner"].title()} Won the Game!")
                        return
                    
                    moves_played = game_event["moves"]
                    if colour == whose_turn(moves_played):
                        print("My Turn to play")

                        # first check if we have moves to play,
                        #   else make draw offer
                        if (num_moves == move_idx):
                            print("Offering Draw\n")
                            draw_accept_or_make_offer(bot_headers, game_id)
                            return

                        move_to_play = moves[move_idx]
                        move_resp = make_move(bot_headers, game_id, move_to_play)
                        if move_resp.status_code == 200:
                            print(f"I played {move_to_play} Successfully\n")
                            move_idx += 1
                        else:
                            print(f"Error playing {move_to_play}\n")
                    else:
                        print("Waiting for opponent...\n")

                elif game_state == "chatLine":

                    # This is sent when a draw is offered
                    message = game_event["text"]
                    user = game_event["username"]
                    print(f"Chat line: '{message}'\nSent from '{user}'\n")

                    # ensure message is sent from user 'lichess'
                    #   and ensure it says '<colour> offers draw'
                    if user == "lichess" and message.split(" ")[-2:] == ["offers", "draw"]:

                        print("Accepting Draw")
                        draw_accept_or_make_offer(bot_headers, game_id)
                        return
                else:
                    # handles any edge cases for game_state
                    print(f"Un-handled Game State: {game_state}")
            else:
                print("keep-alive message received")


def make_move(bot_headers, game_id, move):
    response = re.post(API_URL + f"/bot/game/{game_id}/move/{move}",
                       headers=bot_headers)
    return response

def load_single_game_by_id(id):
    response = re.post(API_URL + "/games/export/_ids",
                       data=id)
    return response


# give in a dict of pgn ids, and a save loacation and this file will export the 
#   game from lichess and create new file in directory
def get_pgns_by_id(ids_dict, dir_to_save):

    for key, val in ids_dict.items():
        resp = load_single_game_by_id(val)
        if resp.status_code == 200:
            # Key has space, but i dont like that so im changing to "-" instead of " "
            key = key.replace(" ", "-") 
            with open(dir_to_save + f"/{key}.pgn", "w") as tf:
                tf.write(resp.text)
            print(key + " Loaded and Saved") 
        else:
            print("Loading of Game ID: ", val, " Failed")
        

def main():

    pass


if __name__ == "__main__":
    main()
