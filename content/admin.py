from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.utils.html import format_html

from content.context import ContextManager
from .models import Sponsorship, Page, Talk, Speaker, Block, Module, ImageInGallery, ImageGallery, ModuleInPage, Style, \
    ListItem, Icon, ButtonInModule, VideoGallery, Room, Language, Button, TalkInGallery

from events.admin import EventModelAdmin, EventTabularInline


class ModuleInline(SortableInlineAdminMixin, EventTabularInline):
    verbose_name_plural = "Modules"
    model = ModuleInPage
    fields = ('order', 'module', 'actions')
    sortable_field_name = "order"
    extra = 3

    def actions(self, instance):
        url = instance.module.get_admin_url()
        return format_html(u'<a class="changelink" href="{}">Change</a>', url)

    readonly_fields = ('actions',)


class ButtonInline(SortableInlineAdminMixin, EventTabularInline):
    verbose_name_plural = "Buttons"
    model = ButtonInModule
    fields = ('order', 'button',)
    sortable_field_name = "order"
    extra = 1


class ImageInline(SortableInlineAdminMixin, EventTabularInline):
    verbose_name_plural = "Images"
    model = ImageInGallery
    fields = ('image', 'order', 'caption', 'as_circle', 'link')
    sortable_field_name = "order"
    extra = 1
    max_num = 8


class TalkInline(SortableInlineAdminMixin, EventTabularInline):
    verbose_name_plural = "Talks"
    model = TalkInGallery
    fields = ('order', 'talk')
    sortable_field_name = "order"
    extra = 3
    max_num = 12


class ListItemInline(SortableInlineAdminMixin, EventTabularInline):
    model = ListItem
    fields = ('icon', 'order', 'title', 'caption')
    sortable_field_name = "order"
    extra = 3
    max_num = 8


class PageAdmin(EventModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'created', 'modified')
    inlines = [ModuleInline, ]


class SponsorshipAdmin(EventModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('context', 'title', 'display_title', 'public', 'subtitle', 'price', 'content',)
        }),
        ('Layout', {
            'fields': ('style', 'content_width')
        }),
        ('Media', {
            'fields': ('image', 'image_position', 'image_on_background')
        }),
    )
    inlines = [ListItemInline, ButtonInline]

    list_display = ('title', 'display_title', 'in_pages', 'modified')

    readonly_fields = ['context', ]

    def context(self, instance):
        cm = ContextManager
        pages_str_list = cm.generate_pages_string(instance)
        return format_html(cm.generate_context(pages_str_list))

    context.allow_tags = True

class BlockAdmin(EventModelAdmin):


    fieldsets = (
        (None, {
            'fields': ('context', 'kicker', 'title', 'display_title', 'public', 'content',)
        }),
        ('Layout', {
            'fields': ('layout', 'style', 'content_width', 'content_justify')
        }),
        ('Media', {
            'fields': ('image', 'image_position', 'image_on_background')
        }),
        ('List', {
            'fields': ('list_title', 'list_style' )
        }),
    )

    list_display = ('title', 'display_title', 'in_pages', 'modified')

    inlines = [ListItemInline, ButtonInline]

    readonly_fields = ['context', ]

    def context(self, instance):
        cm = ContextManager
        pages_str_list = cm.generate_pages_string(instance)
        return format_html(cm.generate_context(pages_str_list))
    context.allow_tags = True

class TalkAdmin(SortableAdminMixin, EventModelAdmin):
    fields = ('title', 'slug', 'content', 'language', 'translation', 'speakers', 'room', 'image', 'video', 'start', 'end' )
    ordering = ('order',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', )


class SpeakerAdmin(EventModelAdmin):
    fields = ('name', 'bio', 'workplace')
    list_display = ('name', 'workplace')


class ImageGalleryAdmin(EventModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('context', 'title', 'display_title', 'public')
        }),
        ('Layout', {
            'fields': ('style',)
        }),
    )

    list_display = ('title', 'display_title', 'in_pages', 'modified')

    inlines = (ImageInline, )

    readonly_fields = ['context', ]

    def context(self, instance):
        cm = ContextManager
        pages_str_list = cm.generate_pages_string(instance)
        return format_html(cm.generate_context(pages_str_list))

    context.allow_tags = True


class VideoGalleryAdmin(EventModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('context', 'title', 'display_title', 'public', 'videos_per_row' )
        }),
        ('Layout', {
            'fields': ('style',)
        }),
    )

    list_display = ('title', 'display_title', 'in_pages', 'modified')

    inlines = (TalkInline, )

    readonly_fields = ['context', ]

    def context(self, instance):
        cm = ContextManager
        pages_str_list = cm.generate_pages_string(instance)
        return format_html(cm.generate_context(pages_str_list))

    context.allow_tags = True

class StyleAdmin(EventModelAdmin):
    fields = ('title', 'slug')
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class IconAdmin(EventModelAdmin):
    exclude = ('event',)


class LanguageAdmin(EventModelAdmin):
    exclude = ('event',)


class RoomAdmin(EventModelAdmin):
    exclude = ('event',)

class ButtonAdmin(EventModelAdmin):
    exclude = ('event',)

admin.site.register(Sponsorship, SponsorshipAdmin)
admin.site.register(Talk, TalkAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(VideoGallery, VideoGalleryAdmin)
admin.site.register(Style, StyleAdmin)
admin.site.register(Icon, IconAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Button, ButtonAdmin)