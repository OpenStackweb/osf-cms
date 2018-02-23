"""
Django settings for osf-cms project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w1n%w0%+uq!#(a58hmi8@w-d!ksv_w07@@0(l=1$kcyr7rvxac'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'content',
    'menus',
    'events',
    'adminsortable2',
    'tinymce',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'osf-cms.middleware.UserAwareFetchFromCacheMiddleware',

]

ROOT_URLCONF = 'osf-cms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/templates/',
            BASE_DIR + '/content/static/katacontainers/templates/'
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



WSGI_APPLICATION = 'osf-cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'file': "/admin/filebrowser/browse?pop",
    'language': "en",
    'gecko_spellcheck' : 'true',
    'dialog_type': "modal",
    'object_resizing': 'true',
    'cleanup_on_startup': 'true',
    'forced_root_block': "p",
    'remove_trailing_nbsp': 'true',
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_statusbar_location': "none",
    'theme_advanced_buttons1': "formatselect,bold,italic,bullist,numlist,hr,link,unlink,anchor,image,separator,undo,redo,separator,removeformat,pastetext,code",
    'theme_advanced_buttons2': "tablecontrols, indent, outdent, justifyleft, justifycenter, justifyright",
    'theme_advanced_buttons3': "",
    'theme_advanced_path': 'false',
    'theme_advanced_resizing' : 'false',
    'theme_advanced_blockformats': 'p,h3,h4,pre',
    'width': '690',
    'height': '350',
    'plugins': "inlinepopups,paste,advimage,table",
    'content_css' : "/static/app/assets/css/tinymce_custom.css",
    'advimage_update_dimensions_onchange': 'true',
    'relative_urls': 'true',
    'convert_urls' : 'true',
    'valid_elements' : "" +
        "-p[class|align]," +
        "a[href|title|id|class|target|align]," +
        "-strong/-b," +
        "-em/-i," +
        "-sup," +
        "-ol," +
        "-ul," +
        "-li," +
        "img[src|alt|width|height]," +
        "br," +
        "hr," +
        "table,thead,tbody,tfoot,th[colspan|rowspan],td[colspan|rowspan],tr," +
        "h3,h4,pre",
}


FILEBROWSER_DIRECTORY = ''
DIRECTORY = ''

FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Icon': ['.svg'],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff',],
    'Document': ['.pdf','.doc','.rtf','.txt','.xls','.csv'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm'],
    'Audio': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p']
}

FILEBROWSER_SELECT_FORMATS = {
    'file': ['Folder','Image','Document','Video','Audio'],
    'image': ['Image'],
    'icon': ['Icon'],
    'icon-image': ['Icon','Image'],
    # 'document': ['Document'],
    'video': ['Video'],
}

CACHES = { # FXIME use STATIC_path
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../static/CACHE')),
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 1800


# Import local settings
try:
    from .settings_local import *
except ImportError:
    print ("Notice: Didn't import settings_local.")
