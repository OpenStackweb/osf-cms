"""opendev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from views import about, sponsors, schedule, videos, faq
from filebrowser.sites import site as filebrowser_site


urlpatterns = [
    url(r'^admin/filebrowser/', filebrowser_site.urls), # filebrowser URLS
    path('admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^home/', about, name='about'),
    url(r'^sponsors/', sponsors, name='sponsors'),
    url(r'^schedule/', schedule, name='schedule'),
    url(r'^videos/', videos, name='videos'),
    url(r'^faq/', faq, name='faq'),
]
