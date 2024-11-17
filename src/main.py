import encrytion as encrypt
import play_a as bot_a
import play_b as bot_b
import sys
import os
import shutil

def config_directory(given_dir_name):
    # First check if given directory name exists and communicate workflow
    current_dirs = os.listdir("src/data")
    if given_dir_name in current_dirs:
        print("Given directory already exists")
        user_inp_to_overwrite = input("Would You Like to overwrite this directory? ([y]/[n]): ").strip()
        if user_inp_to_overwrite == "y" or user_inp_to_overwrite == "Y":
            print("Overwriting directory")
            shutil.rmtree("src/data/" + given_dir_name)
        else:
            print("Directory was not overwritten")
            return

    # ---------------- Create dir structure ---------------- 
    # (see tree in README.md)

    # Set working dir
    working_dir = "src/data/" + given_dir_name
    # Create the directory
    os.mkdir(working_dir)
    # Create secret file to be replaced
    with open(working_dir + "/secret.txt", "w") as tf:
        tf.write("Replace Me\n")

    # Create directory for predifined moves
    os.mkdir(working_dir + "/predefined-moves")
    # Create directory for played games
    os.mkdir(working_dir + "/played-games")


def main():

    args = sys.argv[1:]

    # Ensure we pass in directory name
    if len(args) <= 1:
        print("Invalid Command")
        print("Usage: 'make <command> <directory_name>'")
        return

    if "setup" == args[0]:
        config_directory(args[1])
        return
    elif "encrypt" == args[0]:
        encrypt.encode_secret("src/data/" + args[1])     
    elif "play_a" == args[0]:
        bot_a.play_out_games("src/data/" + args[1])
    elif "play_b" == args[0]:
        bot_b.play_out_games("src/data/" + args[1])
    elif "load" == args[0]:
        bot_a.load_played_games("src/data/" + args[1])
    elif "decrypt" == args[0]:
        encrypt.decode_pgns("src/data/" + args[1])     

        


if __name__ == "__main__":
    main()
