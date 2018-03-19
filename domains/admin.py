from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
from filebrowser.sites import site as filebrowser_site

from domains.models import RedirectHost, CustomSite


class BaseSiteAdmin(admin.ModelAdmin):

    exclude = ('site',)

    def get_queryset(self, request):
        qs = super(BaseSiteAdmin, self).get_queryset(request)
        return self.filter_by_site(qs, request)

    def get_fieldsets(self, request, obj=None):
        filebrowser_site.directory = "uploads/%s/" % request.site.domain
        return super(BaseSiteAdmin, self).get_fieldsets(request, obj)

    def filter_by_site(self, qs, request):
        site = request.site
        return qs.filter(site=site)


    def get_field_queryset(self, db, db_field, request, **kwargs):
        qs = super(BaseSiteAdmin, self).get_field_queryset(db, db_field, request, **kwargs)
        if not qs:  # Django's get_field_queryset may return "None"
            qs = db_field.related_model.objects.all()
        return self.filter_by_site(qs, request)


class SiteModelAdmin(BaseSiteAdmin):
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if getattr(instance, 'event', None) is None:
                instance.site = request.site
            instance.save()
        formset.save_m2m()
        super(SiteModelAdmin, self).save_formset(request, form, formset, change)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'event', None) is None:
            obj.site = request.site
        super(SiteModelAdmin, self).save_model(request, obj, form, change)


class SiteTabularInline(admin.TabularInline):

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(SiteTabularInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        field.queryset = field.queryset.filter(site__id=request.site.id)
        if not field.queryset:
            field.queryset = field.queryset.all()

        return field


class SiteStackedInline(admin.StackedInline):

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(SiteStackedInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        field.queryset = field.queryset.filter(site__id=request.site.id)
        if not field.queryset:
            field.queryset = field.queryset.all()

        return field

class RedirectHostStackedInline(admin.StackedInline):
    model = RedirectHost
    fields = ('redirect_name',)
    extra = 0
    max_num = 8


class CustomSiteAdmin(SiteAdmin):
    inlines = [RedirectHostStackedInline,]

admin.site.unregister(Site)
admin.site.register(CustomSite, CustomSiteAdmin)