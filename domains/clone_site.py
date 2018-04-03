import shutil
from itertools import chain

from django.apps import apps
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
                    attr = obj.__dict__[field.name]
                    attr.path = attr.path.replace('/{}/'.format(self.og_site.domain), '/{}/'.format(self.new_site.domain))
            except Exception as e:
                pass
        return obj

    def clone_and_update_object(self, obj, model, fields):
        old_pk = obj.pk

        obj = self.fix_filebrowser_fields(obj)

        # Module's children are cloned differently
        if obj.__class__.__name__.lower() in ['videogallery', 'imagegallery', 'block', 'sponsorship'
                                            , 'customhtml', 'postcategory', 'modulecontainer']:
            module_model = apps.get_model('content', 'module')
            new_module_pk = self.clone_and_update_object(obj.module_ptr, module_model, fields)
            obj.pk, obj.id = None, None
            obj.module_ptr_id = new_module_pk
            obj.site_id = self.new_site.pk

        elif hasattr(obj, 'site_id'):
            obj.pk, obj.id = None, None
            obj.site_id = self.new_site.pk

        for field in fields:
            if hasattr(obj, field) and getattr(obj, field):
                field_pk = getattr(obj, field).id
                value = self.content[field][field_pk]
                setattr(obj, field + '_id', value)

        obj.save()
        self.content[model._meta.model_name][old_pk] = obj.pk

        return obj.pk

    def clone_and_update_models(self, model, fields):

        instances = model.objects.filter(site_id=self.og_site.pk)
        for obj in instances.iterator():
            self.clone_and_update_object(obj, model, fields)

    def main(self):

        operations = {

            1: ['redirecthost', 'button', 'icon', 'page', 'style'],
            2: ['sitesettings', 'list', 'post', 'bigheadermenu', 'footermenu', 'socialmediamenu'],
            3: ['customhtml', 'postcategory', 'videogallery', 'imagegallery', 'block', 'sponsorship', 'modulecontainer'],
            4: ['buttoninmodule', 'listitem', 'moduleinpage', 'moduleinmodule'],
            5: ['imageingallery',]

        }
        fields = []
        self.clone_uploads_folder()
        model_dict = self.get_models_list()
        del model_dict['module']
        for x in range(1, len(operations) + 1):
            models = operations[x]
            [self.clone_and_update_models(model_dict[model], fields) for model in models]
            fields += models
            if x == 3:
                fields += ['module',]
        pass

    def get_models_list(self):
        generator_content = apps.get_app_config('content').get_models()
        generator_menus = apps.get_app_config('menus').get_models()
        generator_domains = apps.get_app_config('domains').get_models()
        generator = chain(generator_content, generator_menus, generator_domains)
        models_dict = {}
        for model in generator:
            models_dict[model._meta.model_name] = model
            self.content[model._meta.model_name] = {}
        return models_dict


