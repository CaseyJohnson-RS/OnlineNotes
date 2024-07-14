# Этот файл и функция initialize должны присутствовать в каждом
# Модуле для того, чтобы организовать единую точку входа
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from .router_authorization import router as auth_router
from. router_registration import router as regist_router

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def initialize():

    # Здесь тоже твой код
    
    # Всегда возвращаем словарь
    # Обязательные ключи:
    # "routers": []
    return { 
        "routers": [
            auth_router, 
            regist_router
        ] 
    }

def shutdown():

    # И здесь тоже твой код

    # Всегда возвращаем словарь
    return { }

