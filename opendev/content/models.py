from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField

class Page(models.Model):
	title = models.CharField(max_length=50, blank=False)
	slug = models.SlugField()
	content = HTMLField(max_length=65535)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


class Module(models.Model):
	IMAGE_POSITION_CHOICES = (
		('LEFT', 'Left'),
		('RIGHT', 'Right'),
	)
	BACKGROUND_CHOICES = (
		('BLACK', 'Black'),
		('WHITE', 'White'),
		('DARKGREY', 'Dark grey'),
		('LIGHTGREY', 'Light grey'),
		('RED', 'Red'),
		('LIGHTBLUE', 'Light blue'),
	)
	FONT_CHOICES = (
		('BLACK', 'Black'),
		('WHITE', 'White'),
	)
	title = models.CharField(max_length=50, blank=False)
	page = models.ForeignKey(Page, related_name='modules', on_delete=models.SET_NULL, null=True, blank=False)
	order = models.PositiveIntegerField('Order', default=0)
	content = HTMLField(max_length=65535)
	background_color = models.CharField(max_length=9, choices=BACKGROUND_CHOICES, default='BLACK')
	font_color = models.CharField(max_length=9, choices=FONT_CHOICES, default='WHITE')
	image = models.ImageField(blank=True)
	image_position = models.CharField(max_length=6, choices=IMAGE_POSITION_CHOICES, default='LEFT')
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		if self.pk is None:
			page_modules = self.page.modules.all()
			self.order = page_modules.count() + 1
		super(Module, self).save(*args, **kwargs)


	class Meta:
		ordering = ('order',)

	def __str__(self):
		return self.title


class Block(Module):
	LAYOUT_CHOICES = (
		('ONECOL', 'One column'),
		('TWOCOL', 'Two columns'),
	)
	kicker = models.CharField(max_length=50, blank=True)
	layout = models.CharField(max_length=6, choices=LAYOUT_CHOICES, default='ONECOL')


class Sponsorship(Module):
	subtitle = models.CharField(max_length=50, blank=True)
	price = models.FloatField(blank=False)


class ImageGallery(Module):
	class Meta:
		verbose_name_plural = 'Image galleries'

class ImageInGallery(models.Model):
	image = models.ImageField()
	caption = models.CharField(max_length=50, blank=True, null=True)
	gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, related_name='images')
	order = models.PositiveIntegerField('Order', default=0)

	class Meta:
		verbose_name_plural = 'Images in gallery'
		ordering = ('order',)


class Speaker(models.Model):
	name = models.CharField(max_length=50, blank=False)
	bio = models.TextField()
	photo = models.ImageField(blank=True)

	def __str__(self):
		return self.name

class Talk(models.Model):
	title = models.CharField(max_length=50, blank=False)
	content = models.TextField()
	language = models.CharField(max_length=20)
	speakers = models.ManyToManyField(Speaker, related_name='talks')
	room = models.CharField(max_length=30)
	translation = models.BooleanField(default=False)
	photo = models.ImageField(blank=True)
	# slideshare
	# video
	start_time = models.TimeField()
	end_time = models.TimeField()

	def __str__(self):
		return self.title
