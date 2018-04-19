from django.contrib import admin, messages
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
from filebrowser.sites import site as filebrowser_site

from content.models import Page
from domains.models import RedirectHost, SiteSettings


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


class SiteSettingsBaseAdmin(BaseModelAdmin):
    def get_exclude(self, request, obj=None):
        exclude = super(SiteSettingsBaseAdmin, self).get_exclude(request, obj)
        if not obj:
            exclude = ('home_page',)
        return exclude
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['base_site', ]
        return []
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'home_page':
            site_id = request.resolver_match.kwargs['object_id']
            kwargs['queryset'] = Page.objects.filter(site_id=site_id)
        return super(SiteSettingsBaseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SiteSettingsStackedInline(admin.StackedInline, SiteSettingsBaseAdmin):
    model = SiteSettings
    can_delete = False
    extra = 1
    max_num = 1
    verbose_name_plural = 'Settings'
    fk_name = 'site'
    verbose_name = 'Settings'
    

class RedirectHostStackedInline(admin.StackedInline):
    model = RedirectHost
    fields = ('redirect_name',)
    extra = 0
    max_num = 8


class RedirectHostAdmin(BaseSiteAdmin):
    list_display = ['redirect_name', ]
    
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return True
        return False
    
    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return True
        return False
    
    def has_module_permission(self, request):
        if not request.user.is_superuser:
            return True
        return False
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'site') is None:
            obj.site = request.site
        super(RedirectHostAdmin, self).save_model(request, obj, form, change)

    
class SiteSettingsAdmin(admin.ModelAdmin, SiteSettingsBaseAdmin):
    
    list_display = ['site', 'base_site', 'home_page', 'ssl_certified']
    exclude = ['site', ]

    def get_actions(self, request):
        return None

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_module_permission(self, request):
        if not request.user.is_superuser:
            return True
        return False
    
    def get_queryset(self, request):
        qs = super(SiteSettingsAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(site = request.site)
        return qs

    def save_model(self, request, obj, form, change):
        redirect = super(SiteSettingsAdmin, self).save_model(request, obj, form, change)
        obj.site = request.site
        obj.save()
        return redirect


class CustomSiteAdmin(SiteAdmin):
    fields = ['name', 'domain']
    inlines = [SiteSettingsStackedInline, RedirectHostStackedInline]

    def save_model(self, request, obj, form, change):
        redirect = super(CustomSiteAdmin, self).save_model(request, obj, form, change)
        return redirect
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

admin.site.unregister(Site)
admin.site.register(Site, CustomSiteAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(RedirectHost, RedirectHostAdmin)
