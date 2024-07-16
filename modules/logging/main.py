# Этот файл и функция initialize должны присутствовать в каждом
# Модуле для того, чтобы организовать единую точку входа
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from .config import LOGGING, LOG_FILE_PATH
from datetime import datetime

def Log(s: str):

    if LOGGING:
        now = datetime.now()

        file = open(LOG_FILE_PATH, 'a')
        file.write(str(now) + ": " + s + '\n')
        file.close()

routers = []

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def shutdown():

    pass