from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib.admin.options import StackedInline, TabularInline
from django.urls import reverse
from django.utils.html import format_html

from .models import Sponsorship, Page, Talk, Speaker, Block, Module, ImageInGallery, ImageGallery, ModuleInPage, Style, \
	ListItem, Icon, ButtonInModule, VideoInGallery, VideoGallery, Room, Language, Button

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


class VideoInline(SortableInlineAdminMixin, EventTabularInline):
	verbose_name_plural = "Videos"
	model = VideoInGallery
	fields = ('video_url', 'order', 'talk')
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
			'fields': ('title', 'display_title', 'subtitle', 'price', 'content',)
		}),
		('Layout', {
			'fields': ('style', 'content_width')
		}),
		('Media', {
			'fields': ('image', 'image_position', 'image_on_background')
		}),
	)


class BlockAdmin(EventModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('kicker', 'title', 'display_title', 'content',)
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
	inlines = [ListItemInline, ButtonInline]


class TalkAdmin(SortableAdminMixin, EventModelAdmin):
	fields = ('title', 'slug', 'content', 'language', 'translation', 'speakers', 'room', 'image', 'video', 'start', 'end' )
	ordering = ('order',)
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', )


class SpeakerAdmin(EventModelAdmin):
	fields = ('name', 'bio', 'email', 'workplace', 'image')
	list_display = ('name', 'email', 'workplace')


class ImageGalleryAdmin(EventModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('title', 'display_title', )
		}),
		('Layout', {
			'fields': ('style',)
		}),
	)
	inlines = (ImageInline, )


class VideoGalleryAdmin(EventModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('title', 'display_title', 'videos_per_row' )
		}),
		('Layout', {
			'fields': ('style',)
		}),
	)
	inlines = (VideoInline, )


class StyleAdmin(EventModelAdmin):
	fields = ('title', 'slug')
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