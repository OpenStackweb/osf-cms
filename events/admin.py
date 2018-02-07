from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from content.models import Module
from events.models import Event
from filebrowser.sites import site as filebrowser_site


class EventAdmin(admin.ModelAdmin):
	fields = ('title', 'slug', 'logo', 'start_date', 'public', 'custom_css', 'base_event')
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'slug', 'start_date', 'public' )

	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ['base_event',]
		return []

class BaseEventAdmin(admin.ModelAdmin):

	exclude = ('event',)

	def get_queryset(self, request):
		qs = super(BaseEventAdmin, self).get_queryset(request)
		return self.filter_by_event(qs, request)

	def get_fieldsets(self, request, obj=None):
		filebrowser_site.directory = "uploads/%s/" % request.META['HTTP_HOST'].split('.')[0]
		return super(BaseEventAdmin, self).get_fieldsets(request, obj)

	def filter_by_event(self, qs, request):
		event = self.get_event_or_404(request)
		return qs.filter(event=event)

	def get_event_or_404(self, request):
		event_slug = request.META['HTTP_HOST'].split('.')[0]
		return get_object_or_404(Event, slug=event_slug)

	def get_field_queryset(self, db, db_field, request, **kwargs):
		qs = super(BaseEventAdmin, self).get_field_queryset(db, db_field, request, **kwargs)
		if not qs:  # Django's get_field_queryset may return "None"
			qs = db_field.related_model.objects.all()
		return self.filter_by_event(qs, request)


class EventModelAdmin(BaseEventAdmin):
	def save_formset(self, request, form, formset, change):
		instances = formset.save(commit=False)
		for instance in instances:
			if getattr(instance, 'event', None) is None:
				instance.event = self.get_event_or_404(request)
			instance.save()
		formset.save_m2m()
		super(EventModelAdmin, self).save_formset(request, form, formset, change)

	def save_model(self, request, obj, form, change):
		if getattr(obj, 'event', None) is None:
			obj.event = self.get_event_or_404(request)
		super(EventModelAdmin, self).save_model(request, obj, form, change)


class EventTabularInline(admin.TabularInline):

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(EventTabularInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

		field.queryset = field.queryset.filter(event__slug=request.META['HTTP_HOST'].split('.')[0])
		if not field.queryset:
			field.queryset = field.queryset.all()

		return field


class EventStackedInline(admin.StackedInline):

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(EventStackedInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

		field.queryset = field.queryset.filter(event__slug=request.META['HTTP_HOST'].split('.')[0])
		if not field.queryset:
			field.queryset = field.queryset.all()

		return field


admin.site.register(Event, EventAdmin)
