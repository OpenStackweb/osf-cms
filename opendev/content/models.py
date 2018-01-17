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
	WIDTH_CHOICES = (
		('WIDE', 'Wide'),
		('SEMIWIDE', 'Semiwide'),
		('NARROW', 'Narrow'),
	)
	TYPE_CHOICES = (
		('BLOCK', 'Block'),
		('SPONSOR', 'Sponsorship'),
		('IMAGEGALLERY', 'Image gallery'),
	)
	title = models.CharField(max_length=50)
	display_title = models.BooleanField(default=True)
	content = HTMLField(max_length=65535, blank=True)
	content_width = models.CharField(max_length=8, choices=WIDTH_CHOICES, default='WIDE')
	style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)
	image = FileBrowseField(max_length=200, directory='assets', format='Image', blank=True, null=True)
	image_position = models.CharField(max_length=6, choices=IMAGE_POSITION_CHOICES, default='LEFT')
	image_on_background = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	type = models.CharField(max_length=12, choices=TYPE_CHOICES, null=True)

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
	STYLE_CHOICES = (
		('NONE', 'None'),
		('VERTICALSEP', 'Vertical separators'),
		('HORIZONTALSEP', 'Horizontal separator on top'),
		('VERTICALHORIZONTAL', 'Vertical + horizontal separator'),
	)
	list_title = models.CharField(max_length=50, blank=True)
	list_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='None')
	kicker = models.CharField(max_length=50, blank=True)
	layout = models.CharField(max_length=6, choices=LAYOUT_CHOICES, default='ONECOL')

	def save(self, *args, **kwargs):
		is_new = False
		if self.pk is None:
			is_new = True
		super(Block, self).save(*args, **kwargs)
		if is_new:
			module = self.module_ptr
			module.type = 'BLOCK'
			module.save()


class Sponsorship(Module):
	subtitle = models.CharField(max_length=50, blank=True)
	price = models.FloatField(blank=False)

	def save(self, *args, **kwargs):
		is_new = False
		if self.pk is None:
			is_new = True
		super(Sponsorship, self).save(*args, **kwargs)
		if is_new:
			module = self.module_ptr
			module.type = 'SPONSOR'
			module.save()


class ImageGallery(Module):

	def save(self, *args, **kwargs):
		is_new = False
		if self.pk is None:
			is_new = True
		super(ImageGallery, self).save(*args, **kwargs)
		if is_new:
			module = self.module_ptr
			module.type = 'IMAGEGALLERY'
			module.save()
	class Meta:
		verbose_name_plural = 'Image galleries'


class ImageInGallery(models.Model):
	image = FileBrowseField(max_length=200, directory='assets', format='Image', blank=True, null=True)
	caption = models.CharField(max_length=50, blank=True, null=True)
	gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, related_name='images')
	order = models.PositiveIntegerField('Order', default=0)

	class Meta:
		verbose_name_plural = 'Images in gallery'
		ordering = ('order',)


class Speaker(models.Model):
	name = models.CharField(max_length=50, blank=False)
	bio = models.TextField()
	image = FileBrowseField(max_length=200, directory='assets', format='Image', blank=True, null=True)

	def __str__(self):
		return self.name

class Talk(models.Model):
	title = models.CharField(max_length=50, blank=False)
	content = models.TextField()
	language = models.CharField(max_length=20)
	speakers = models.ManyToManyField(Speaker, related_name='talks')
	room = models.CharField(max_length=30)
	translation = models.BooleanField(default=False)
	image = FileBrowseField(max_length=200, directory='assets', format='Image', blank=True, null=True)
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


class Icon(models.Model):
	name = models.CharField(max_length=25, blank=False)
	image = FileBrowseField(max_length=200, directory="images", format='Icon', blank=True, null=True)

	def __str__(self):
		return self.name

class ListItem(models.Model):
	icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True, blank=True)
	title = models.CharField(max_length=50, blank=True, null=True)
	caption = models.CharField(max_length=200, blank=True, null=True)
	module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='list_items')
	order = models.PositiveIntegerField('Order', default=0)

	class Meta:
		verbose_name_plural = 'List items'
		ordering = ('order',)

	def __str__(self):
		return "{} ({})".format(self.caption, self.module.title)


class Button(models.Model):
	caption = models.CharField(max_length=40, blank=False)
	url = models.URLField()

	def __str__(self):
		return "{} ({})".format(self.caption, self.url)


class ButtonInModule(models.Model):
	button = models.ForeignKey(Button, on_delete=models.CASCADE)
	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	order = models.PositiveIntegerField('Order', default=0)

	class Meta:
		ordering = ['order',]
		verbose_name = "Module"

	def __str__(self):
		return "{} ({})".format(self.button.caption, self.module.title)