# Этот файл и функция initialize должны присутствовать в каждом
# Модуле для того, чтобы организовать единую точку входа
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from .router_authorization import router as auth_router
from. router_registration import router as regist_router

routers = [
    auth_router, 
    regist_router
] 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def shutdown():

    # Здесь твой код

    # Всегда возвращаем словарь
    pass

