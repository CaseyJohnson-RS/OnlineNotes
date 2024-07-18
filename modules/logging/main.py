# Этот файл и функция initialize должны присутствовать в каждом
# Модуле для того, чтобы организовать единую точку входа
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from .config import LOGGING, LOG_FILE_PATH
from datetime import datetime

def LogTime():

    if LOGGING:
        now = datetime.now()

        msg = '\n' + str(now)

        file = open(LOG_FILE_PATH, 'a')
        file.write(msg + '\n')
        print(msg)
        file.close()

def Log(s: str):

    if LOGGING:

        file = open(LOG_FILE_PATH, 'a')
        file.write(str(s) + '\n')
        print(str(s))
        file.close()

routers = []

LogTime()
Log("Start logging")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def shutdown():

    pass