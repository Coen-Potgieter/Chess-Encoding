import os
import shutil

def config_directory(given_dir_name, overwrite=False):
    # First check if given directory name exists and communicate workflow
    current_dirs = os.listdir("src/data")
    if given_dir_name in current_dirs:
        print("Given directory already exists")
        if not overwrite:
            print("if you would like to overwrite this directory set the `overwrite` parameter to `True`")
            return
        else:
            print("Overwriting directory")
            shutil.rmtree("src/data/" + given_dir_name)

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
    config_directory("fooTest")


if __name__ == "__main__":
    main()
