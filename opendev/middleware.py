from django.middleware.cache import FetchFromCacheMiddleware


class UserAwareFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    def process_request(self, request):
        if request.user.is_staff:
            # force a full page request, skip cache
            return None
        return super(UserAwareFetchFromCacheMiddleware, self).process_request(request)
