from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from domains.admin import SiteModelAdmin
from .models import BigHeaderMenu, FooterMenu, SocialMediaMenu

# TOFIX implement EventModelAdmin as SiteModelAdmin instead of admin.ModelAdmin
class MenuSortableAdmin(SortableAdminMixin, SiteModelAdmin):
    list_display = ('display_name', 'get_target')
    ordering=('order', )

    def get_target(self, obj):
        if obj.target_type == 'page':
            return 'Page: %s' % obj.page
        elif obj.target_type == 'url':
            return obj.url
        else:
            return obj.target_type

    get_target.short_description = 'target'

class SocialMediaMenuSortableAdmin(SortableAdminMixin, SiteModelAdmin):
    fields = ('display_name', 'url', 'social_network')
    list_display = ('display_name', 'url')
    ordering=('order', )



admin.site.register(BigHeaderMenu, MenuSortableAdmin)
admin.site.register(FooterMenu, MenuSortableAdmin)
admin.site.register(SocialMediaMenu, SocialMediaMenuSortableAdmin)
