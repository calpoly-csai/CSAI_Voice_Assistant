'''
Name: Nimbus CLI
Author: Jason Ku
Date:
Organization: Cal Poly CSAI
Description: Provides a CLI tool to easily access Nimbus training features
'''

import AddPath
import Audio_Data_Recording
import False_Activation_Extractor
import Scrape_Gutenburg_Audio
import Train_Model


def main():
    response = ""
    confirm = ""

    while not response == "e":
        print("What would you like to do?")
        print("* (p) to add or edit the repository (p)ath")
        print("* (r) to (r)ecord audio")
        print("* (s) to (s)crape Gutenburg audio")
        print("* (f) to extract (f)alse activation data")
        print("* (t) to (t)rain a model")
        print("* (e) to (e)xit")

        response = input().lower()
        print()

        # AddPath script
        if (response == "p"):
            AddPath.main()

        # Audio_Data_Recording script
        elif (response == "r"):
            while not confirm == "y":
                print("Enter your username (this will be used to label your audio recordings).")
                username = input()
                print("You entered: " + username + ". Is this correct? (y)es or (n)o")
                confirm = input().lower()

            Audio_Data_Recording.main(username)
            print()

        # Scrape_Gutenburg_Audio script
        elif (response == "s"):
            while not confirm == "y":
                print("Enter the Gutenburg audio link")
                link = input()
                print("You entered: \"" + link + "\". Is this correct? (y)es or (n)o")
                confirm = input().lower()

            try:
                Scrape_Gutenburg_Audio.main(['scrape_gutenburg_audio.py', link])
            except Exception as e:
                print(e)
            print()

        # False_Activation_Extractor script
        elif (response == "f"):
            while not confirm == "y":
                try:
                    print(False_Activation_Extractor.main(["-h"]))
                except:
                    # do nothing
                    print()

                print("\nEnter arguments with flags: ")

                args = input().split()
                print("\nYou entered:")
                print(' '.join(args))
                print("Is this correct? (y)es or (n)o")
                confirm = input().lower()

            try:
                False_Activation_Extractor.main(args)
            except Exception as e:
                print(e)
            print()

        # Train_Model script
        elif (response == "t"):
            try:
                Train_Model.main()
            except Exception as e:
                print(e)
            print()

        elif (response == "e"):
            break

        else:
            print("\nYour input \"" + response + "\" was not recognized.\n")

    print("\nExiting...")


if __name__ == '__main__':
    main()
