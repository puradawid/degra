"""
Django settings for degra project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-lmq22b5%fr7y)*jni!u_ys-2l0$rnk5b&c)r(f_n@78au8-ws'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    ##### Default apps ######
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ##### Third party apps #####
    'widget_tweaks',
    #'south',
    'password_reset',
)

## HERE ADD OUR REAL APPS ##
PROJECT_APPS = (
    'apps.plan',
    'apps.accounts',
    'apps.panel',
)

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',                          
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'degra.urls'

WSGI_APPLICATION = 'degra.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    STATIC_PATH,
)

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

TEMPLATE_DIRS = (
     TEMPLATE_PATH,
)

# E-Mail configuration
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'planyzajec2014@gmail.com'
EMAIL_HOST_PASSWORD = 'degra2.0'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# LDAP configuration     
# http://pythonhosted.org/django-auth-ldap/     
                
# LDAP     
import ldap    
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, LDAPSearchUnion    
    
AUTHENTICATION_BACKENDS = (    
'django_auth_ldap.backend.LDAPBackend',    
'django.contrib.auth.backends.ModelBackend',    
)    
    
AUTH_LDAP_SERVER_URI = "ldaps://ldap.wi.pb.edu.pl:10636"    
    
AUTH_LDAP_BIND_DN = ""    
AUTH_LDAP_BIND_PASSWORD = ""    
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=people,ou=FCS,o=BUT,c=pl", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")    
    
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()    
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=wierkgroups,ou=groups,ou=FCS,o=BUT,c=pl", ldap.SCOPE_SUBTREE
, "(objectClass=groupOfNames)"    )    
    
AUTH_LDAP_USER_ATTR_MAP = {"email": "mail", "first_name": "givenName", "last_name": "sn"}     
    
AUTH_LDAP_USER_FLAGS_BY_GROUP = {    
"is_staff": "cn=admins,ou=wierkgroups,ou=groups,ou=FCS,o=BUT,c=pl",    
"is_superuser": "cn=superusers,ou=wierkgroups,ou=groups,ou=FCS,o=BUT,c=pl",    
# "is_active": "cn=admins,ou=wierkgroups,ou=groups,ou=FCS,o=BUT,c=pl",     
# "ou=employees,ou=people,ou=FCS,o=BUT,c=pl",     
}

AUTH_LDAP_BIND_DN = "uid=nawiaagent,ou=agents,ou=FCS,o=BUT,c=pl"
AUTH_LDAP_BIND_PASSWORD = "Nawia2014"    
    
AUTH_LDAP_ALWAYS_UPDATE_USER = True    
    
AUTH_LDAP_MIRROR_GROUPS=True 
