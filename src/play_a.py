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

    # make challenge to bot B
    api.make_challenge(HEADERS, "freeMemory2")

    # wait for challenge accept
    event = api.listen_to_events(HEADERS)
    if event["state"] == api.EventState.GAME_START:
        # game started
        game_id = event["id"]
        print(f"Game {game_id} started!")

    elif event["state"] == api.EventState.GAME_DECLINED:
        # if game is declined then make the challenge again
        api.make_challenge(HEADERS, "freeMemory2")
    

if __name__ == "__main__":
    main()
