from django.contrib.admin import site
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.utils.html import format_html
from nested_admin.nested import NestedStackedInline, NestedTabularInline, NestedModelAdmin

from content.context import ContextManager
from .models import Sponsorship, Page, Block, Module, ImageInGallery, ImageGallery, ModuleInPage, Style, \
    ListItem, Icon, ButtonInModule, VideoGallery, Button, CustomHTML, PostCategory, Post, ModuleInModule, \
    ModuleContainer, List

# TOFIX: Single site fixing
# from events.admin import EventModelAdmin, EventTabularInline
from django.contrib.admin import TabularInline as EventTabularInline
from django.contrib.admin import StackedInline as EventStackedInline
from django.contrib.admin import ModelAdmin as EventModelAdmin


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
    

class ModuleContainerInline(SortableInlineAdminMixin, EventTabularInline):
    verbose_name_plural = "Modules"
    model = ModuleInModule
    fk_name = 'container'
    fields = ('order', 'module',)
    sortable_field_name = "order"
    extra = 2


class ImageInline(SortableInlineAdminMixin, EventTabularInline):
    verbose_name_plural = "Images"
    model = ImageInGallery
    fields = ('image', 'order', 'caption', 'as_circle', 'link')
    sortable_field_name = "order"
    extra = 1
    max_num = 28
    

# class TalkInline(SortableInlineAdminMixin, EventTabularInline):
#     verbose_name_plural = "Talks"
#     model = TalkInGallery
#     fields = ('order', 'talk')
#     sortable_field_name = "order"
#     extra = 3
#     max_num = 12


class ListItemInline(NestedTabularInline):
    model = ListItem
    sortable_field_name = "order"
    # fields = ('icon', 'title', 'caption')
    extra = 1
    max_num = 8


class ListStackedInline(NestedTabularInline):
    model = List
    extra = 0
    # exclude = ('order',)
    inlines = [ListItemInline, ]
    sortable_field_name = "order"
    max_num = 2


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
    inlines = [ButtonInline,]

    list_display = ('title', 'display_title', 'in_pages', 'modified')

    readonly_fields = ['context', ]

    def context(self, instance):
        cm = ContextManager
        pages_str_list = cm.generate_pages_string(instance)
        return format_html(cm.generate_context(pages_str_list))

    context.allow_tags = True


class BlockAdmin(NestedModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('context', 'kicker', 'title', 'display_title', 'title_only', 'public', 'content',)
        }),
        ('Layout', {
            'fields': ('layout', 'style', 'content_width', 'content_justify')
        }),
        ('Media', {
            'fields': ('image', 'image_position', 'image_on_background')
        }),
    )

    list_display = ('title', 'display_title', 'in_pages', 'modified')

    inlines = [ListStackedInline, ButtonInline]

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


class ImageGalleryAdmin(EventModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('context', 'title', 'display_title', 'public')
        }),
        ('Layout', {
            'fields': ('style', 'images_per_row')
        }),
    )

    list_display = ('title', 'display_title', 'in_pages', 'modified', 'images_per_row')

    inlines = (ImageInline, )

    readonly_fields = ['context', ]

    def context(self, instance):
        cm = ContextManager
        pages_str_list = cm.generate_pages_string(instance)
        return format_html(cm.generate_context(pages_str_list))

    context.allow_tags = True
    

class PostCategoryAdmin(EventModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('context', 'title', 'display_title', 'public',)
        }),
        ('Layout', {
            'fields': ('style',)
        }),
    )

    list_display = ('title', 'display_title', 'in_pages', 'modified',)

    readonly_fields = ['context', ]

    def context(self, instance):
        cm = ContextManager
        pages_str_list = cm.generate_pages_string(instance)
        return format_html(cm.generate_context(pages_str_list))

    context.allow_tags = True


class CustomHTMLAdmin(EventModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('context', 'kicker', 'title', 'display_title', 'public', 'html_block')
        }),
        ('Layout', {
            'fields': ('style',)
        }),
    )

    list_display = ('title', 'display_title', 'in_pages', 'modified')

    readonly_fields = ['context', ]

    def context(self, instance):
        cm = ContextManager
        pages_str_list = cm.generate_pages_string(instance)
        return format_html(cm.generate_context(pages_str_list))

    context.allow_tags = True
    

class ModuleContainerAdmin(EventModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('context', 'title', 'display_title', 'public',)
        }),
        ('Layout', {
            'fields': ('style',)
        }),
    )

    list_display = ('title', 'display_title', 'in_pages', 'modified')

    readonly_fields = ['context', ]
    
    inlines = (ModuleContainerInline, )
    
    def context(self, instance):
        cm = ContextManager
        pages_str_list = cm.generate_pages_string(instance)
        return format_html(cm.generate_context(pages_str_list))

    context.allow_tags = True

# class VideoGalleryAdmin(EventModelAdmin):
#     fieldsets = (
#         (None, {
#             'fields': ('context', 'title', 'display_title', 'public', 'videos_per_row' )
#         }),
#         ('Layout', {
#             'fields': ('style',)
#         }),
#     )
#
#     list_display = ('title', 'display_title', 'in_pages', 'modified')
#
#     inlines = (TalkInline, )
#
#     readonly_fields = ['context', ]
#
#     def context(self, instance):
#         cm = ContextManager
#         pages_str_list = cm.generate_pages_string(instance)
#         return format_html(cm.generate_context(pages_str_list))
#
#     context.allow_tags = True

class StyleAdmin(EventModelAdmin):
    fields = ('title', 'slug')
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    
class PostAdmin(EventModelAdmin):
    fields = ('title', 'slug', 'author', 'date', 'image', 'content', 'categories')
    list_display = ('title', 'slug', 'author', 'date',)
    prepopulated_fields = {'slug': ('title',)}


class IconAdmin(EventModelAdmin):
    exclude = ('event',)


class LanguageAdmin(EventModelAdmin):
    exclude = ('event',)


class RoomAdmin(EventModelAdmin):
    exclude = ('event',)

class ButtonAdmin(EventModelAdmin):
    exclude = ('event',)


# site.register(Sponsorship, SponsorshipAdmin)
site.register(Page, PageAdmin)
site.register(Block, BlockAdmin)
site.register(ImageGallery, ImageGalleryAdmin)
site.register(PostCategory, PostCategoryAdmin)
site.register(CustomHTML, CustomHTMLAdmin)
site.register(Style, StyleAdmin)
site.register(Icon, IconAdmin)
site.register(Button, ButtonAdmin)
site.register(Post, PostAdmin)
site.register(ModuleContainer, ModuleContainerAdmin)