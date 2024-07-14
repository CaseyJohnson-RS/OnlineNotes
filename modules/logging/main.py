# Этот файл и функция initialize должны присутствовать в каждом
# Модуле для того, чтобы организовать единую точку входа
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from .config import LOGGING, LOG_FILE_PATH

def Log(s: str):

    if LOGGING:
        file = open(LOG_FILE_PATH, 'a')
        file.write(s + '\n')
        file.close()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def initialize():
    
    # Всегда возвращаем словарь
    # Обязательные ключи:
    # "routers": []
    return { 
        "routers": []
    }

def shutdown():

    # Всегда возвращаем словарь
    return { }