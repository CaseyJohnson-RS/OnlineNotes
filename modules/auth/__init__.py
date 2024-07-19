from .routers.authorization import router as auth_router
from .routers.registration import router as regist_router
from .routers.restore_password import router as restore_pass_router

routers = [
    auth_router, 
    regist_router,
    restore_pass_router
] 

