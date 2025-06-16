import os

from config.components.base import BASE_DIR

# Основная конфигурация логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Не отключаем существующие логгеры
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {filename}:{lineno} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),  # Путь к файлу логов
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'INFO',
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'errors.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'loggers': {
        '': {  # Корневой логгер
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {  # Логгер для Django
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'faceid': {  # Логгер для приложения
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Создание директории для логов, если она не существует
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)
