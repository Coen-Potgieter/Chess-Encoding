import requests as re
import dotenv
import os
import json

dotenv.load_dotenv()

TOKEN_A = os.getenv('BOT_A_TOKEN')
TOKEN_B = os.getenv('BOT_B_TOKEN')


def upgrade():
    headers_a = {"Authorization": f"Bearer {TOKEN_A}"}
    headers_b = {"Authorization": f"Bearer {TOKEN_B}"}

    upgrade_a_resp = re.post("https://lichess.org/api/bot/account/upgrade", 
                             headers=headers_a)

    if upgrade_a_resp.status_code == 200:
        print("Bot A has been upgraded")
    else:
        print("Something went wrong")
        print(upgrade_a_resp.json())

    upgrade_b_resp = re.post("https://lichess.org/api/bot/account/upgrade", 
                             headers=headers_b)
    
    if upgrade_b_resp.status_code == 200:
        print("Bot B has been upgraded")
    else:
        print("Something went wrong")

def accountStatus(token):

    headers = {"Authorization": f"Bearer {token}"}
    response = re.get("https://lichess.org/api/account", headers=headers)
    
    if response.status_code == 200:
        json_content = response.json()
        for key, val in json_content.items():
            print(key, " -> ", val)


def main():
    upgrade()
    accountStatus(TOKEN_A)
    print()
    accountStatus(TOKEN_B)


if __name__ == "__main__":
    main()
