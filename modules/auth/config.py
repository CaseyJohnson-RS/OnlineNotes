from os import getenv

# Алгоритм хеширования паролей
ALGORITHM = getenv('ALGORITHM')

# Время в минутах, сколько действителен токен доступа
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Время в минутах, сколько сервер готов ждать подтверждения регистрации
REGIST_CONFIRM_EXPIRE_MINUTES = int(getenv('REGIST_CONFIRM_EXPIRE_MINUTES'))

# Время в минутах, сколько сервер готов ждать подтверждения восстановления пароля
RESTORE_CONFIRM_EXPIRE_MINUTES = int(getenv('RESTORE_CONFIRM_EXPIRE_MINUTES'))

# Время в минутах, сколько сервер готов ждать новый пароль после подтверждения восстановления
NEW_PASSWORD_WAIT_EXPIRE_MINUTES = int(getenv('NEW_PASSWORD_WAIT_EXPIRE_MINUTES'))

# Почтовый ящик, с которого будет отправлятся рассылка
# Это надо как-то заменить
EMAIL_SENDER_ADDRESS = getenv('EMAIL_SENDER_ADDRESS')
EMAIL_SENDER_PASSWORD = getenv('EMAIL_SENDER_PASSWORD')