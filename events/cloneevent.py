import shutil

from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

from events.models import Event
import opendev.settings as settings


class CloneViewSet:
	def __init__(self, og_event, new_event):
		self.og_event = og_event
		self.new_event_name = new_event.name
		self.new_event = new_event
		self.new_event_pk = new_event.pk
		self.content = {}

	def clone_uploads_folder(self):
		try:
			shutil.copytree(settings.MEDIA_ROOT + '/uploads/{}/'.format(self.og_event.slug), settings.MEDIA_ROOT + "/uploads/{}/".format(self.new_event.slug))
		except OSError:
			pass

	def clone_and_update_models(self, model, fields):

		instances = model.objects.prefetch_related('pk', 'event_id').filter(event_id=self.og_event.pk)
		for obj in instances.iterator():
			old_pk = obj.pk
			obj.pk = None
			if hasattr(obj, 'event_id'):
				obj.event_id = self.new_event_pk
			for field in fields:
				if hasattr(obj, field) and getattr(obj, field):
					field_pk = getattr(obj, field).id
					value = self.content[field][field_pk]
					setattr(obj, field + '_id', value)
				# elif hasattr(obj, field + '_id') and getattr(obj, field + '_id'):
				#         field_pk = getattr(obj, field + '_id')
				#         value = self.content[field][field_pk.id]
				#         setattr(obj, field + '_id_id', value)
				# if hasattr(obj, 'parent_' + field) and getattr(obj, 'parent_' + field):
				#     field_pk = getattr(obj, 'parent_' + field )
				#     value = self.content[field][field_pk.id]
				#     setattr(obj, 'parent_' + field + '_id', value)
			obj.save()
			self.content[model._meta.model_name][old_pk] = obj.pk





	def main(self):
		# THIS WORKS UP TO NOW
		# self.new_hotel_pk = 50
		operations = {
			1: ['speaker', 'room', 'language', 'button', 'icon', 'page', 'style'],
			2: ['module', 'talk'],
			3: ['buttoninmodule', 'listitem', 'moduleinpage', 'videogallery', 'imagegallery', 'block', 'sponsorship'],
			4: ['videoingallery', 'imageingallery',]

		}
		fields = []
		self.clone_uploads_folder()
		model_dict = self.get_models_list()
		for x in range(1, len(operations) + 1):
			models = operations[x]
			[self.clone_and_update_models(model_dict[model], fields) for model in models]
			fields += models
		pass

	def get_models_list(self):
		generator = apps.get_app_config('content').get_models()
		models_dict = {}
		for model in generator:
			models_dict[model._meta.model_name] = model
			self.content[model._meta.model_name] = {}
		return models_dict


@receiver(post_save, sender=Event)
def clone_hotel(sender, **kwargs):
	if kwargs['created']:
		cvs = CloneViewSet(kwargs['instance'].base_event, kwargs['instance'])
		cvs.main()