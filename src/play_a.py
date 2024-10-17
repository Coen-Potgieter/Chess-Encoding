import api
import dotenv
import os
import sys
import json

dotenv.load_dotenv()

TOKEN_A = os.getenv('BOT_A_TOKEN')
HEADERS = {"Authorization": f"Bearer {TOKEN_A}"}


def load_moves(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def list_challenges():
    api.print_pretty_json(api.list_challenges(HEADERS))
    sys.exit()


def main():

    # for debugging
    # list_challenges()

    # clear all challenges and abort all ongoing games
    api.clear_all_challenges(HEADERS)
    api.resign_all_games(HEADERS)

    game_started = False
    game_id = None

    # Phase 1 is getting a game started
    while not game_started:
        # make challenge to bot B
        api.make_challenge(HEADERS, "freeMemory2")

        # wait for challenge accept
        event = api.listen_to_events(HEADERS)
        if event["state"] == api.EventState.GAME_START:

            # game started
            game_id = event["id"]
            print(f"Game {game_id} started!")
            game_started = True
        else:
            # If anything is returned other than GAME_START we make challenge
            #   again
            pass

    moves = load_moves("src/data/predefinedMoves/Game1/white.json")
    print(moves)
    # Phase 2 once a game is started we play the game
    game_ongoing = True
    while game_ongoing:
        if api.wait_until_my_move(HEADERS):
            print("My turn to move")
            api.make_move(HEADERS, game_id, moves[0])



if __name__ == "__main__":
    main()
