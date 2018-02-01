from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from events.admin import EventModelAdmin
from .models import BigHeaderMenu, FooterMenu


class MenuSortableAdmin(SortableAdminMixin, EventModelAdmin):
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


admin.site.register(BigHeaderMenu, MenuSortableAdmin)
admin.site.register(FooterMenu, MenuSortableAdmin)
