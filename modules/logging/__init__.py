from .config import LOGGING, LOG_FILE_PATH

def Log(s: str):

    if LOGGING:

        file = open(LOG_FILE_PATH, 'a')
        file.write(str(s) + '\n')
        print(str(s))
        file.close()


Log("Start logging")

