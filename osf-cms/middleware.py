from django.apps import apps
from django.contrib.sites.models import Site
from django.contrib.sites.requests import RequestSite
from django.middleware.cache import FetchFromCacheMiddleware
from django.utils.deprecation import MiddlewareMixin

from domains.models import RedirectHost, CustomSite


class UserAwareFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    def process_request(self, request):
        if request.user.is_staff:
            # force a full page request, skip cache
            return None
        return super(UserAwareFetchFromCacheMiddleware, self).process_request(request)


class SiteRedirectMiddleware(MiddlewareMixin):
    def get_current_site(self, request):
        """
        Check if contrib.sites is installed and return either the current
        ``Site`` object or a ``RequestSite`` object based on the request.
        """
        # Imports are inside the function because its point is to avoid importing
        # the Site models when django.contrib.sites isn't installed.
        if apps.is_installed('django.contrib.sites'):
            return Site.objects.get_current(request).custom_site
        else:
            return RequestSite(request)

    def process_request(self, request):
        try:
            request.site = self.get_current_site(request)
        except Site.DoesNotExist:
            domain_name = request.META['HTTP_HOST'].replace(':' + request.META['SERVER_PORT'], '')
            redirect = RedirectHost.objects.get(redirect_name=domain_name)
            request.site = CustomSite.objects.get(id=redirect.site_id)

