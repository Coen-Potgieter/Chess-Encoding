import api
import dotenv
import os
import sys

dotenv.load_dotenv()

TOKEN_B = os.getenv('BOT_B_TOKEN')
HEADERS = {"Authorization": f"Bearer {TOKEN_B}"}


def list_challenges():
    api.print_pretty_json(api.list_challenges(HEADERS))
    sys.exit()


def main():

    # for debugging
    # list_challenges()

    my_colour = api.Colour.BLACK

    # Wait for challenge from bot A
    event = api.listen_to_events(HEADERS)

    game_id = None

    if event["state"] == api.EventState.CHALLENGE:
        # now accept the challenge
        game_id = event["id"]
        api.accept_challenge(HEADERS, game_id)

    moves = api.load_moves("src/data/predefinedMoves/scholarsMate.json")["black"]

    # Phase 2 once a game is started we play the game
    api.play_game(HEADERS, game_id, moves, my_colour)


if __name__ == "__main__":
    main()
