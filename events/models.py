from django.db import models


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
