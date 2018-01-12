from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib.admin.options import StackedInline, TabularInline

from .models import Sponsorship, Page, Talk, Speaker, Block, Module, ImageInGallery, ImageGallery, ModuleInPage, Style, \
	ListItem


class ModuleInline(SortableInlineAdminMixin, TabularInline):
	model = ModuleInPage
	fields = ('order', 'module')
	sortable_field_name = "order"
	extra = 3


class ImageInline(SortableInlineAdminMixin, TabularInline):
	model = ImageInGallery
	fields = ('image', 'order', 'caption')
	sortable_field_name = "order"
	extra = 1
	max_num = 8


class ListItemInline(SortableInlineAdminMixin, TabularInline):
	model = ListItem
	fields = ('icon', 'order', 'caption')
	sortable_field_name = "order"
	extra = 1
	max_num = 8


class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'slug', 'created', 'modified')
	inlines = [ModuleInline, ]


class SponsorshipAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('title', 'display_title', 'subtitle', 'price', 'content',)
		}),
		('Layout', {
			'fields': ('style', )
		}),
		('Media', {
			'fields': ('image', 'image_position', 'image_on_background')
		}),
	)

class BlockAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('kicker', 'title', 'display_title', 'content',)
		}),
		('Layout', {
			'fields': ('layout', 'style')
		}),
		('Media', {
			'fields': ('image', 'image_position', 'image_on_background')
		}),
		('List', {
			'fields': ('list_title', 'display_list')
		}),
	)
	inlines = [ListItemInline,]


class TalkAdmin(admin.ModelAdmin):
	fields = ('title', 'content', 'language', 'translation', 'speakers', 'room', 'photo', 'start_time', 'end_time' )
	list_display = ('title', 'language', 'room')


class SpeakerAdmin(admin.ModelAdmin):
	fields = ('name', 'bio')


class ImageGalleryAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('title', 'display_title', )
		}),
		('Layout', {
			'fields': ('style',)
		}),
	)
	inlines = (ImageInline, )


class StyleAdmin(admin.ModelAdmin):
	fields = ('title', 'slug')
	prepopulated_fields = {'slug': ('title',)}


admin.site.register(Sponsorship, SponsorshipAdmin)
admin.site.register(Talk, TalkAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(ImageGallery, ImageGalleryAdmin)
admin.site.register(Style, StyleAdmin)