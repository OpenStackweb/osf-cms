from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib.admin.options import StackedInline, TabularInline

from .models import Sponsorship, Page, Talk, Speaker, Block, Module, ImageInGallery, ImageGallery


class ModuleInline(SortableInlineAdminMixin, StackedInline):
	model = Module
	sortable_field_name = "order"
	extra = 0


class ImageInline(SortableInlineAdminMixin, TabularInline):
	model = ImageInGallery
	fields = ('image', 'order', 'caption')
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
			'fields': ('page', 'title', 'subtitle', 'price', 'content',)
		}),
		('Layout', {
			'fields': ('background_color', 'font_color',)
		}),
		('Media', {
			'fields': ('image', 'image_position')
		}),
	)

class BlockAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('page', 'kicker', 'title', 'content',)
		}),
		('Layout', {
			'fields': ('layout', 'background_color', 'font_color',)
		}),
		('Media', {
			'fields': ('image', 'image_position')
		}),
	)

class TalkAdmin(admin.ModelAdmin):
	fields = ('title', 'content', 'language', 'translation', 'speakers', 'room', 'photo', 'start_time', 'end_time' )
	list_display = ('title', 'language', 'room')


class SpeakerAdmin(admin.ModelAdmin):
	fields = ('name', 'bio')

class ImageGalleryAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('page', 'title', )
		}),
		('Layout', {
			'fields': ('background_color', 'font_color',)
		}),
	)
	inlines = (ImageInline, )

admin.site.register(Sponsorship, SponsorshipAdmin)
admin.site.register(Talk, TalkAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(ImageGallery, ImageGalleryAdmin)