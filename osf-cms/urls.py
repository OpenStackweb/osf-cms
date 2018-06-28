"""osf-cms URL Configuration

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
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, include
from django.views.generic import RedirectView

from content.views import PageView, HomeView, filebrowser_browse, filebrowser_base, ClearCache, PostView
from filebrowser.sites import site as filebrowser_site

filebrowser_url = [
    url(r'^admin/filebrowser/browse/$', filebrowser_browse, name="fb_browse"),
    url(r'^admin/filebrowser/upload/$', filebrowser_base('upload'), name="fb_upload"),
    url(r'^admin/filebrowser/createdir/$',filebrowser_base('createdir'), name="fb_createdir"),
    url(r'^admin/filebrowser/delete_confirm/$', filebrowser_base('delete_confirm'), name="fb_delete_confirm"),
    url(r'^admin/filebrowser/delete/$', filebrowser_base('delete'), name="fb_delete"),
    url(r'^admin/filebrowser/detail/$', filebrowser_base('detail'), name="fb_detail"),
    url(r'^admin/filebrowser/version/$', filebrowser_base('version'), name="fb_version"),
]
urlpatterns = filebrowser_url + [
    url(r'^admin/clear-cache/$', staff_member_required(ClearCache.as_view()), name='clear-cache'),

    url(r'^admin/filebrowser/', filebrowser_site.urls), # filebrowser URLS
    path('admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^posts/(?P<post_slug>[-\w]+)?/$', PostView.as_view(), name='post'),
    url(r'^(?P<slug>[-\w]+)?/$', PageView.as_view(), name='page'),
    url(r'^(?P<slug>[-\w]+)/(?P<year>[-\w]+)?/$', PageView.as_view(), name='posts_year'),
    url(r'^(?P<slug>[-\w]+)/tags/(?P<tag>[-\w]+)?/$', PageView.as_view(), name='posts_by_tag'),

    url(r'^select2/', include('django_select2.urls')),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

