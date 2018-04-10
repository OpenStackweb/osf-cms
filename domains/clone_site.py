import shutil
from itertools import chain

import itertools
from django.apps import apps
from django.core.exceptions import FieldError
from django.db import connection
from django.db.models import ForeignKey, OneToOneField
from filebrowser.fields import FileBrowseField

from django.conf import settings



class CloneViewSet:
    def __init__(self, og_site, new_site):
        self.og_site = og_site
        self.new_site = new_site
        self.content = {}

    def clone_uploads_folder(self):
        try:
            shutil.copytree(settings.MEDIA_ROOT + '/uploads/{}/'.format(self.og_site.domain), settings.MEDIA_ROOT + "/uploads/{}/".format(self.new_site.domain))
        except OSError:
            pass

    def fix_filebrowser_fields(self, obj):
        for field in obj._meta.fields:
            try:
                if isinstance(field, FileBrowseField):
                    attr = getattr(obj, field.name)
                    attr.path = attr.path.replace('/{}/'.format(self.og_site.domain), '/{}/'.format(self.new_site.domain))
            except Exception as e:
                pass
        return obj

    def set_new_fk_values(self, obj, app_model = False):
        fields = [field for field in list(obj._meta.model._meta.get_fields()) if (isinstance(field, ForeignKey) or isinstance(field, OneToOneField))]

        from content.models import Module
        if app_model and not isinstance(obj, Module):
            old_key = [k for k in self.content[obj._meta.model._meta.model_name] if
                           self.content[obj._meta.model._meta.model_name][k] == obj.id][0]
            
            old_obj = obj._meta.model.objects.get(id=old_key)
        else:
            old_obj = obj

        for field in fields:
            if field.attname not in ['site_id', 'module_ptr_id']:
                value = getattr(old_obj, field.attname.replace('_id', ''))
                if value:
                    value_model_name = value._meta.model_name
                    new_id = self.content[value_model_name][value.id]
                    setattr(obj, field.attname, new_id)
        return obj

    def update_objects(self):
        for model in self.apps_models:
            instances = model.objects.filter(site=self.new_site)
            for obj in instances:
                obj = self.set_new_fk_values(obj, app_model=True)
                obj.save()
            
    def set_foreign_keys_null(self, obj):
        for field in obj._meta.model._meta.get_fields():
            if isinstance(field, OneToOneField):
                setattr(obj, field.attname, None)
        return obj

    def clone_auto_created_objects(self):
        for model in self.auto_created_models:
            instances = model.objects.all()
            for obj in instances:
                obj.pk, obj.id = None, None
                obj = self.set_new_fk_values(obj)
                obj.save()
            
    def clone_apps_objects(self):
        self.content['module'] = {}
        for model in self.apps_models:
            model_name = model._meta.model_name
            self.content[model_name] = {}
            instances = model.objects.filter(site=self.og_site)
            for obj in instances:
                old_pk = obj.pk
                obj = self.fix_filebrowser_fields(obj)
                obj.pk, obj.id = None, None
                obj = self.set_foreign_keys_null(obj)
                obj.site_id = self.new_site.pk
                obj.save()
                from content.models import Module
                # Modules are created automatically when creating its children.
                if isinstance(obj, Module):
                    self.content['module'][old_pk] = obj.pk
                self.content[model_name][old_pk] = obj.pk
                
    def get_home_page(self):
        og_home_page_id = self.og_site.settings.home_page.id
        new_home_page_id = self.content['page'][og_home_page_id]
        return new_home_page_id
    

    def main(self):
        self.clone_uploads_folder()
        self.auto_created_models, self.apps_models = self.get_models_list()
        self.clone_apps_objects()
        self.clone_auto_created_objects()
        self.update_objects()
        return self.get_home_page()
        
    def get_models_list(self):
        generator_content = apps.get_app_config('content').get_models(include_auto_created=True)
        generator_menus = apps.get_app_config('menus').get_models(include_auto_created=True)
        generator_domains = apps.get_app_config('domains').get_models(include_auto_created=True)
        generator_redirects = apps.get_app_config('redirects').get_models(include_auto_created=True)
        auto_created_models, apps_models = itertools.tee(chain(generator_content
                                                               , generator_menus,
                                                               generator_domains, generator_redirects), 2)
        auto_created_models = [model for model in auto_created_models if model._meta.auto_created]
        apps_models = [model for model in apps_models if (model._meta.model_name.lower() not in ['sitesettings', 'module', 'redirecthost'] and not model._meta.auto_created)]
        return auto_created_models, apps_models

