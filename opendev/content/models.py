from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from filebrowser.fields import FileBrowseField
from tinymce.models import HTMLField

class Page(models.Model):
	title = models.CharField(max_length=50, blank=False)
	slug = models.SlugField()
	content = HTMLField(max_length=65535, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


class Style(models.Model):
	title = models.CharField(max_length=50, blank=False)
	slug = models.SlugField(blank=False, null=False)

	def __str__(self):
		return self.title


class Module(models.Model):
	IMAGE_POSITION_CHOICES = (
		('LEFT', 'Left'),
		('RIGHT', 'Right'),
	)
	title = models.CharField(max_length=50)
	display_title = models.BooleanField(default=True)
	content = HTMLField(max_length=65535, blank=True)
	style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)
	image = FileBrowseField(max_length=200, directory='assets', format='Image', blank=True, null=True)
	image_position = models.CharField(max_length=6, choices=IMAGE_POSITION_CHOICES, default='LEFT')
	image_on_background = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	# def save(self, *args, **kwargs):
	# 	if self.pk is None:
	# 		page_modules = self.page.modules.all()
	# 		self.order = page_modules.count() + 1
	# 	super(Module, self).save(*args, **kwargs)

	def __str__(self):
		return self.title


class Block(Module):
	LAYOUT_CHOICES = (
		('ONECOL', 'One column'),
		('TWOCOL', 'Two columns'),
	)
	list_title = models.CharField(max_length=50, blank=True)
	display_list = models.BooleanField(default=False)
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


class ModuleInPage(models.Model):
	module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='modules_in_page')
	page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='modules_in_page')
	order = models.PositiveIntegerField('Order', default=0)

	class Meta:
		ordering = ['order',]
		verbose_name = "Module"

	def __str__(self):
		return "{} ({})".format(self.module.title, self.page.title)


class ListItem(models.Model):
	icon = FileBrowseField(max_length=200, directory="images", format='Image', blank=True, null=True)
	caption = models.CharField(max_length=50, blank=True, null=True)
	module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='list_items')
	order = models.PositiveIntegerField('Order', default=0)

	class Meta:
		verbose_name_plural = 'List items'
		ordering = ('order',)