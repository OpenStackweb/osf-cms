from django.db import models


class Event(models.Model):
	title = models.CharField(max_length=50, blank=False)
	slug = models.SlugField(unique=True)
	start_date = models.DateField(blank=False)
	public = models.BooleanField(default=True)


class BaseEventModel(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='%(class)ss')

	class Meta:
		abstract = True
