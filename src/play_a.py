import api
import dotenv
import os
import sys
import json

dotenv.load_dotenv()

TOKEN_A = os.getenv('BOT_A_TOKEN')
HEADERS = {"Authorization": f"Bearer {TOKEN_A}"}


def list_challenges():
    api.print_pretty_json(api.list_challenges(HEADERS))
    sys.exit()

def play_out_games(path_to_json, path_to_save_ids):

    # for debugging
    # list_challenges()

    # clear all challenges and abort all ongoing games
    api.clear_all_challenges(HEADERS)
    api.resign_all_games(HEADERS)
    my_colour = api.Colour.WHITE

    loaded_games = api.load_moves(path_to_json)
    games = loaded_games.values()
    ids_of_played_games = {}
    # Cycle through each game
    for game_idx, game in enumerate(games):

        # flags for game handling
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
                # If anything is else returned other than GAME_START we make
                #   challenge again
                pass

        moves_to_play = game["white"]

        # Phase 2 once a game is started we play the game
        api.play_game(HEADERS, game_id, moves_to_play, my_colour)
        # Save Game ID so we can pull pgn from site later
        ids_of_played_games[f"Game {game_idx + 1}"] = game_id

        print(f"-------------------- Game {game_idx + 1} Completed ------------------- ")

    with open(path_to_save_ids, "w") as tf:
        json.dump(ids_of_played_games, tf, indent=4)


def load_played_games(dir_of_ids):
    with open(dir_of_ids + "/ids.json", "r") as tf:
        game_ids = json.load(tf)

    api.get_pgns_by_id(game_ids, dir_of_ids)
    return

def main():
    # play_out_games("src/data/test1/predefined-moves/moves.json", "src/data/test1/played-games/ids.json")
    load_played_games("src/data/test1/played-games")

    






if __name__ == "__main__":
    main()
