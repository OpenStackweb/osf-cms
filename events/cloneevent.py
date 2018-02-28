import shutil
from itertools import chain

from django.apps import apps
from filebrowser.fields import FileBrowseField

from django.conf import settings

class CloneViewSet:
    def __init__(self, og_event, new_event):
        self.og_event = og_event
        self.new_event_name = new_event.title
        self.new_event = new_event
        self.new_event_pk = new_event.pk
        self.content = {}

    def clone_uploads_folder(self):
        try:
            shutil.copytree(settings.MEDIA_ROOT + '/uploads/{}/'.format(self.og_event.slug), settings.MEDIA_ROOT + "/uploads/{}/".format(self.new_event.slug))
        except OSError:
            pass

    def fix_filebrowser_fields(self, obj):
        for field in obj._meta.fields:
            try:
                if isinstance(field, FileBrowseField):
                    attr = obj.__dict__[field.name]
                    attr.path = attr.path.replace('/{}/'.format(self.og_event.slug), '/{}/'.format(self.new_event.slug))
            except:
                pass
        return obj

    def clone_and_update_object(self, obj, model, fields):
        old_pk = obj.pk

        obj = self.fix_filebrowser_fields(obj)

        if obj.__class__.__name__.lower() in ['videogallery', 'imagegallery', 'block', 'sponsorship']:
            module_model = apps.get_model('content', 'module')
            new_module_pk = self.clone_and_update_object(obj.module_ptr, module_model, fields)
            obj.pk, obj.id = None, None
            obj.module_ptr_id = new_module_pk
            obj.event_id = self.new_event_pk

        elif hasattr(obj, 'event_id'):
            obj.pk, obj.id = None, None
            obj.event_id = self.new_event_pk

        for field in fields:
            if hasattr(obj, field) and getattr(obj, field):
                field_pk = getattr(obj, field).id
                value = self.content[field][field_pk]
                setattr(obj, field + '_id', value)

        obj.save()
        self.content[model._meta.model_name][old_pk] = obj.pk

        return obj.pk

    def clone_and_update_models(self, model, fields):

        instances = model.objects.filter(event_id=self.og_event.pk)
        for obj in instances.iterator():
            self.clone_and_update_object(obj, model, fields)

    def main(self):

        operations = {

            1: ['button', 'icon', 'page', 'style'],
            2: ['post', 'bigheadermenu', 'footermenu', 'socialmediamenu'],
            3: ['customhtml', 'postcategory', 'videogallery', 'imagegallery', 'block', 'sponsorship'],
            4: ['buttoninmodule', 'listitem', 'moduleinpage', 'moduleinmodule', 'modulecontainer'],
            5: ['talkingallery', 'imageingallery',]

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
        generator = chain(generator_content, generator_menus)
        models_dict = {}
        for model in generator:
            models_dict[model._meta.model_name] = model
            self.content[model._meta.model_name] = {}
        return models_dict


