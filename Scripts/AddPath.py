'''
Name: Path Adder
Author: Chidi
Date: 10/10/2019
Organization: Cal Poly CSAI
Description: Adds the path to the CSAI Voice Assistant
             directory for the program scripts

'''
import json
import os

from Utils.OS_Find import Path_OS_Assist


def main():
    path = ""  # path string
    confirm = ""  # confirms
    path_json = {}
    delim = Path_OS_Assist()

    while (path == ""):
        temp = input("Enter the path to the CSAI_Voice_Assistant repository "
                     "in your local machine: ")

        while not(confirm.lower() == "n" or confirm.lower() == "y"):
            print("Please confirm that this is the path you "
                  "would like to add:\n\n Path: %s" % temp)
            print("\n\n(y) for yes | (n) for no")
            confirm = input()

            if (confirm == "y"):
                path = temp

    path_json["PATH"] = path

    with open(os.getcwd() + "%sUtils%sPATH.json" % (delim, delim), "w") \
            as in_json:
        json.dump(path_json, in_json)
        print("Path %s has been added to Utils/PATH.json. If an error has "
              "occurred, you can run the program again and reinsert the path")


if __name__ == "__main__":
    main()
