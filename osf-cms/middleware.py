import re

from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.middleware.cache import FetchFromCacheMiddleware
from django.template.defaultfilters import lower
from django.utils.deprecation import MiddlewareMixin
from pip import logger


class UserAwareFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    def process_request(self, request):
        if request.user.is_staff:
            # force a full page request, skip cache
            return None
        return super(UserAwareFetchFromCacheMiddleware, self).process_request(request)


class SiteRedirectMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        try:
            request.site = get_current_site(request)
        except:
            sites = Site.objects.all()
            domain_name = request.META['HTTP_HOST'].replace(':' + request.META['SERVER_PORT'], '')
            for site in sites:
                redirects = site.redirect_hosts.all().filter(redirect_name=domain_name)
                if redirects:
                    request.site = redirects.first().site