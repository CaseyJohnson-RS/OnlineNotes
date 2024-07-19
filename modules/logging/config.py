from os import getenv

LOGGING = bool(getenv('LOGGING'))
LOG_FILE_PATH = getenv('LOG_FILE_PATH')