import os


def Path_OS_Assist():

    if(os.name == "nt"):
        delim = "\\"

    else:
        delim = "/"

    return delim
