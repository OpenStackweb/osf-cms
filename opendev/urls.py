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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from content.views import PageView, HomeView, TalkView
from filebrowser.sites import site as filebrowser_site


urlpatterns = [
    url(r'^admin/filebrowser/', filebrowser_site.urls), # filebrowser URLS
    path('admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^(?P<slug>[-\w]+)?/$', PageView.as_view(), name='page'),
    url(r'^talk/(?P<slug>[-\w]+)?/$', TalkView.as_view(), name='talk'),

    url(r'^faq/', RedirectView.as_view(url="/media/assets/opendev-faq_081617.pdf"), name='faq'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
