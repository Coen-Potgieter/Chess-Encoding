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

    # Wait for challenge from bot A
    event = api.listen_to_events(HEADERS)

    if event["state"] == api.EventState.CHALLENGE:
        # now accept the challenge
        api.accept_challenge(HEADERS, event["id"])

    print(event["state"])


if __name__ == "__main__":
    main()
