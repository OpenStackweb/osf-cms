from django.contrib import admin
from django.shortcuts import get_object_or_404

from content.models import Module
from events.models import Event
from filebrowser.sites import site as filebrowser_site


class EventAdmin(admin.ModelAdmin):
	fields = ('title', 'slug', 'start_date', 'public', 'base_event')
	prepopulated_fields = {'slug': ('title',)}
	list_display = ('title', 'slug', 'start_date', 'public' )


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


class BaseEventInline():

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		kwargs["queryset"] = Module.objects.filter(event__slug=request.META['HTTP_HOST'].split('.')[0])
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

class EventTabularInline(BaseEventInline, admin.TabularInline):
	pass


class EventStackedInline(BaseEventInline, admin.StackedInline):
	pass


admin.site.register(Event, EventAdmin)
