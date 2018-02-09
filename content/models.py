from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from filebrowser.fields import FileBrowseField
from tinymce.models import HTMLField
from events.models import BaseEventModel

class Page(BaseEventModel):
    title = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(unique=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        if not self.slug:
            return reverse('home')

        return reverse('page', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Style(BaseEventModel):
    title = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(unique=False, blank=False, null=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('title',)



class Module(BaseEventModel):
    IMAGE_POSITION_CHOICES = (
        ('LEFT', '◧ Left'),
        ('RIGHT', '◨ Right'),
    )
    WIDTH_CHOICES = (
        ('WIDE', '█ Wide'),
        ('SEMIWIDE', '▌ Semi wide'),
        ('NARROW', '▎ Narrow'),
    )
    TYPE_CHOICES = (
        ('BLOCK', 'Block'),
        ('SPONSORSHIP', 'Sponsorship'),
        ('IMAGEGALLERY', 'Image gallery'),
        ('VIDEOGALLERY', 'Video gallery')
    )
    title = models.CharField(max_length=50)
    display_title = models.BooleanField(default=True)
    content = HTMLField(max_length=65535, blank=True)
    content_width = models.CharField(max_length=8, choices=WIDTH_CHOICES, default='WIDE')
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)
    image = FileBrowseField(max_length=200, directory='images', format='Image', blank=True, null=True)
    image_position = models.CharField(max_length=6, choices=IMAGE_POSITION_CHOICES, default='LEFT')
    image_on_background = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=12, choices=TYPE_CHOICES, null=True)

    def in_pages(self):  # For admin
        return ", ".join(Page.objects.filter(modules_in_page__module=self).values_list('title', flat=True))

    def get_admin_url(self):
        """the url to the Django admin interface for the model instance"""
        return reverse('admin:%s_%s_change' % (self._meta.app_label,
                                              self.type.lower()),
                                                args=(self.id,))
    def save(self, *args, **kwargs):
        is_new = False
        if self.pk is None:
            is_new = True
        super(Module, self).save(*args, **kwargs)
        if is_new and not self.type:
            module = self.module_ptr
            module_type = type(self).__name__.upper()
            module.type = module_type
            module.save()

    def __str__(self):
        return self.title


class Block(Module):
    LAYOUT_CHOICES = (
        ('ONECOL', '□ One column'),
        ('TWOCOL', '◫ Two columns'),
    )
    STYLE_CHOICES = (
        ('NONE', 'None'),
        ('VERTICALSEP', 'Vertical separators'),
        ('HORIZONTALSEP', 'Horizontal separator on top'),
        ('VERTICALHORIZONTAL', 'Vertical + horizontal separator'),
    )
    ALIGN_CHOICES = (
        ('LEFT', '⯇ Left'),
        ('CENTER', '￭ Center'),
        ('RIGHT', '⯈ Right')
    )

    list_title = models.CharField(max_length=50, blank=True)
    list_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='None')
    kicker = models.CharField(max_length=50, blank=True)
    layout = models.CharField(max_length=6, choices=LAYOUT_CHOICES, default='ONECOL')
    content_justify = models.CharField('Content align', max_length=6, choices=ALIGN_CHOICES, default='LEFT')

    def __str__(self):
        return "{} {}".format(self.kicker, self.title)


class Sponsorship(Module):
    subtitle = models.CharField(max_length=50, blank=True)
    price = models.FloatField(blank=False)



class ImageGallery(Module):

    class Meta:
        verbose_name_plural = 'Image galleries'


class VideoGallery(Module):

    videos_per_row = models.IntegerField(default=3, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Video galleries'


class ImageInGallery(BaseEventModel):
    image = FileBrowseField(max_length=200, directory='images', format='Image', blank=True, null=True)
    as_circle = models.BooleanField(default=False, blank=False, null=False)
    caption = models.CharField(max_length=50, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    imagegallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, related_name='images')
    order = models.PositiveIntegerField('Order', default=0)

    class Meta:
        verbose_name_plural = 'Images in gallery'
        ordering = ('order',)


class Speaker(BaseEventModel):
    name = models.CharField(max_length=50, blank=False)
    bio = HTMLField(max_length=65535, blank=True)
    workplace = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    image = FileBrowseField(max_length=200, directory='images/speakers', format='Image', blank=True, null=True)

    def __str__(self):
        return self.name


class Room(BaseEventModel):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name

class Language(BaseEventModel):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name

class Talk(BaseEventModel):
    title = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(unique=False, blank=False, null=True)
    content = HTMLField(max_length=65535, blank=False )
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    speakers = models.ManyToManyField(Speaker, related_name='talks')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    translation = models.BooleanField(default=False)
    image = FileBrowseField(max_length=200, directory='images/talks', format='Image', blank=True, null=True)
    # slideshare
    video = models.URLField(blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    order = models.PositiveIntegerField('Order', default=0)

    class Meta:
        ordering = ['order',]

    def get_absolute_url(self):
        if not self.slug:
            return reverse('talk')

        return reverse('talk', kwargs={'slug': self.slug})


    def __str__(self):
        return self.title


class VideoInGallery(BaseEventModel):
    video_url = models.URLField(blank=False, null=False)
    videogallery = models.ForeignKey(VideoGallery, on_delete=models.CASCADE, related_name='videos')
    talk = models.ForeignKey(Talk, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    order = models.PositiveIntegerField('Order', default=0)

    class Meta:
        verbose_name_plural = 'Videos in gallery'
        ordering = ('order',)

class ModuleInPage(BaseEventModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='modules_in_page')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='modules_in_page')
    order = models.PositiveIntegerField('Order', default=0)

    class Meta:
        ordering = ['order',]
        verbose_name = "Module"

    def __str__(self):
        return "{} ({})".format(self.module.title, self.page.title)


class Icon(BaseEventModel):
    name = models.CharField(max_length=25, blank=False)
    image = FileBrowseField(max_length=200, directory="images/icons", format='Icon', blank=True, null=True)

    def __str__(self):
        return self.name

class ListItem(BaseEventModel):
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


class Button(BaseEventModel):
    caption = models.CharField(max_length=40, blank=False)
    url = models.URLField()

    def __str__(self):
        return "{}".format(self.caption)


class ButtonInModule(BaseEventModel):
    button = models.ForeignKey(Button, on_delete=models.CASCADE, related_name='modules')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='buttons')
    order = models.PositiveIntegerField('Order', default=0)

    class Meta:
        ordering = ['order',]
        verbose_name = "Module"

    def __str__(self):
        return "{} ({})".format(self.button.caption, self.module.title)