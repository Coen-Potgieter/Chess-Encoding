import api
import dotenv
import os
import sys
import time

dotenv.load_dotenv()

TOKEN_B = os.getenv('BOT_B_TOKEN')
HEADERS = {"Authorization": f"Bearer {TOKEN_B}"}


def list_challenges():
    api.print_pretty_json(api.list_challenges(HEADERS))
    sys.exit()


def play_out_games(path_to_dir):

    # for debugging
    # list_challenges()

    my_colour = api.Colour.BLACK


    loaded_games = api.load_moves(path_to_dir + "/predefined-moves/moves.json")
    games = loaded_games.values()
    for game_idx, game in enumerate(games):
        game_id = None
        # Wait for challenge from bot A

        while game_id is None:
            event = api.listen_to_events(HEADERS)
            if event["state"] == api.EventState.CHALLENGE:
                # now accept the challenge
                game_id = event["id"]
                api.accept_challenge(HEADERS, game_id)

        moves_to_play = game["black"] 

        # Phase 2 once a game is started we play the game
        api.play_game(HEADERS, game_id, moves_to_play, my_colour)
        
        print(f"-------------------- Game {game_idx + 1} Completed ------------------- ")


def main():

    start = time.time()
    play_out_games("src/data/imgTest")
    end = time.time()
    print(f"Encoding Took {end - start}s")




if __name__ == "__main__":
    main()
