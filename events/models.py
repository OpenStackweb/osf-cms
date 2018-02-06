from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from events.cloneevent import CloneViewSet


class Event(models.Model):
	title = models.CharField(max_length=50, blank=False)
	slug = models.SlugField(unique=True)
	start_date = models.DateField(blank=False)
	public = models.BooleanField(default=True)
	base_event = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Clone from')

	def __str__(self):
		return self.title

class BaseEventModel(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='%(class)ss')

	class Meta:
		abstract = True

@receiver(post_save, sender=Event)
def clone_hotel(sender, **kwargs):
	if kwargs['created']:
		cvs = CloneViewSet(kwargs['instance'].base_event, kwargs['instance'])
		cvs.main()