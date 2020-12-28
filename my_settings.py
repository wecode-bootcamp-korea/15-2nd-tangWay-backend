DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tangway',
        'USER': 'root',
        'PASSWORD': "",
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
SECRET_KEY = 'pqztd6zb@6ce2op2+wg0qac-%155r8&bz^ujeqonr77ifybs@-'
JWT_ALGORITHM = "HS256"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}


