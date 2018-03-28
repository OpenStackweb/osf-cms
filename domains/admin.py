from django.contrib import admin, messages
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


class SiteSettingsStackedInline(admin.StackedInline):
    model = SiteSettings
    can_delete = False
    extra = 1
    max_num = 1
    verbose_name_plural = 'Settings'
    fk_name = 'site'
    verbose_name = 'Settings'
    
    def get_exclude(self, request, obj=None):
        exclude = super(SiteSettingsStackedInline, self).get_exclude(request, obj)
        if not obj:
            exclude = ('home_page',)
        return exclude
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'home_page':
            site_id = request.resolver_match.kwargs['object_id']
            kwargs['queryset'] = Page.objects.filter(site_id=site_id)
        return super(SiteSettingsStackedInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class RedirectHostStackedInline(admin.StackedInline):
    model = RedirectHost
    fields = ('redirect_name',)
    extra = 0
    max_num = 8


class CustomSiteAdmin(SiteAdmin):
    fields = ['name', 'domain']
    inlines = [SiteSettingsStackedInline, ]

    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(CustomSiteAdmin, self).get_inline_instances(request, obj)
    
    def save_model(self, request, obj, form, change):
        redirect = super(CustomSiteAdmin, self).save_model(request, obj, form, change)
        messages.warning(request, 'Remember to assign a Home Page to your new site for it to work properly.')
        return redirect


admin.site.unregister(Site)
admin.site.register(Site, CustomSiteAdmin)
