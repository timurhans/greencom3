# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'YOUR SECRET KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['192.168.18.5','0.0.0.0']
# ALLOWED_HOSTS = ['172.16.1.2','0.0.0.0']
# ALLOWED_HOSTS = ['192.168.2.100','0.0.0.0']


ALLOWED_HOSTS = ['191.238.216.168','0.0.0.0']
#ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
