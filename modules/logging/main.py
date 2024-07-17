# Этот файл и функция initialize должны присутствовать в каждом
# Модуле для того, чтобы организовать единую точку входа
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from .config import LOGGING, LOG_FILE_PATH
from datetime import datetime

def LogTime():

    if LOGGING:
        now = datetime.now()

        file = open(LOG_FILE_PATH, 'a')
        file.write('\n' + str(now) + ": \n")
        file.close()

def Log(s: str):

    if LOGGING:

        file = open(LOG_FILE_PATH, 'a')
        file.write(str(s) + '\n')
        file.close()

routers = []

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def shutdown():

    pass