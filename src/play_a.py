import api
import dotenv
import os
import sys

dotenv.load_dotenv()

TOKEN_A = os.getenv('BOT_A_TOKEN')
HEADERS = {"Authorization": f"Bearer {TOKEN_A}"}


def list_challenges():
    api.print_pretty_json(api.list_challenges(HEADERS))
    sys.exit()


def main():

    # for debugging
    # list_challenges()

    # clear all challenges and abort all ongoing games
    api.clear_all_challenges(HEADERS)
    api.resign_all_games(HEADERS)
    my_colour = api.Colour.WHITE

    loaded_games = api.load_moves("src/data/predefinedMoves/message1.json")
    games = loaded_games.values()

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

        print(f"-------------------- Game {game_idx + 1} Completed ------------------- ")


if __name__ == "__main__":
    main()
