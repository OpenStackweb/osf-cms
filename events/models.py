from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from filebrowser.fields import FileBrowseField

from events.cloneevent import CloneViewSet


class Event(models.Model):
	title = models.CharField(max_length=50, blank=False)
	slug = models.SlugField(unique=True)
	logo = FileBrowseField(max_length=200, directory='logos', format='Image', blank=True, null=True)
	start_date = models.DateField(blank=False)
	public = models.BooleanField(default=True)
	custom_css = models.TextField(blank=True, null=True, verbose_name='Custom CSS')
	base_event = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Clone from')

	def __str__(self):
		return self.title

class BaseEventModel(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='%(class)ss')

	class Meta:
		abstract = True

@receiver(post_save, sender=Event)
def clone_hotel(sender, **kwargs):
	if kwargs['created'] and kwargs['instance'].base_event:
		cvs = CloneViewSet(kwargs['instance'].base_event, kwargs['instance'])
		cvs.main()