import logging.config

from src.config.settings import settings

_configuration = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': '%(levelname)s - %(asctime)s - %(name)s - %(message)s'}
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
        },
    },
}

if settings.DEBUG:
    _configuration['loggers']['sqlalchemy.engine'] = {  # type: ignore[index]
        'handlers': ['default'],
        'level': 'INFO',
    }

logging.config.dictConfig(_configuration)

logger = logging.getLogger('delivery')
