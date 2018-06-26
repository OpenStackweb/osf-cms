from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from filebrowser.fields import FileBrowseField
from tagulous.models import TagField
from tinymce.models import HTMLField

class Page(models.Model):
    title = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(unique=False, blank=True)
    public = models.BooleanField(default=True, help_text="If unchecked, only logged-in users can see this page")
    excerpt = models.TextField(max_length=350, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        if not self.slug:
            return reverse('home')

        return reverse('page', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Style(models.Model):
    title = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(unique=False, blank=False, null=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('title',)



class Module(models.Model):
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
        ('VIDEOGALLERY', 'Video gallery'),
        ('POSTCATEGORY', 'Post category'),
        ('CUSTOMHTML', 'Custom HTML'),
        ('MODULECONTAINER', 'Module container')
    )
    title = models.CharField(max_length=80)
    display_title = models.BooleanField(default=True)
    public = models.BooleanField(default=True, help_text="If unchecked, only logged-in users can see this module")
    content = HTMLField(max_length=65535, blank=True)
    content_width = models.CharField(max_length=8, choices=WIDTH_CHOICES, default='WIDE')
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)
    image = FileBrowseField(max_length=200, directory='images', format='Image', blank=True, null=True)
    image_position = models.CharField(max_length=6, choices=IMAGE_POSITION_CHOICES, default='LEFT')
    image_on_background = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True)

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

    ALIGN_CHOICES = (
        ('LEFT', '⯇ Left'),
        ('CENTER', '￭ Center'),
        ('RIGHT', '⯈ Right')
    )
    title_only = models.BooleanField(default=False)
    kicker = models.CharField(max_length=50, blank=True)
    layout = models.CharField(max_length=6, choices=LAYOUT_CHOICES, default='ONECOL')
    content_justify = models.CharField('Content align', max_length=6, choices=ALIGN_CHOICES, default='LEFT')

    def __str__(self):
        return "{} {}".format(self.kicker, self.title)


class Sponsorship(Module):
    subtitle = models.CharField(max_length=50, blank=True)
    price = models.FloatField(blank=False)


class ImageGallery(Module):

    images_per_row = models.IntegerField(default=3, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Image galleries'


class VideoGallery(Module):

    videos_per_row = models.IntegerField(default=3, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Video galleries'
        
class PostCategory(Module):
    
    class Meta:
        verbose_name_plural = 'Post categories'
        
        
class ModuleContainer(Module):
    
    class Meta:
        verbose_name_plural = 'Module containers'
        
class CustomHTML(Module):
    html_block = models.TextField()
    kicker = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Custom HTML blocks'

class ImageInGallery(models.Model):
    image = FileBrowseField(max_length=200, directory='images', format='icon-image', blank=True, null=True)
    as_circle = models.BooleanField(default=False, blank=False, null=False)
    caption = models.CharField(max_length=50, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    imagegallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, related_name='images')
    order = models.PositiveIntegerField('Order', default=0)

    class Meta:
        verbose_name_plural = 'Images in gallery'
        ordering = ('order',)


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
    image = FileBrowseField(max_length=200, directory="images/icons", format='Icon', blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=25, blank=False)

    def __str__(self):
        return self.name


class List(models.Model):
    STYLE_CHOICES = (
        ('NONE', 'None'),
        ('VERTICALSEP', 'Vertical separators'),
        ('HORIZONTALSEP', 'Horizontal separator on top'),
        ('VERTICALHORIZONTAL', 'Vertical + horizontal separator'),
        ('INCOLUMNS', 'Display in two columns')
    )
    title = models.CharField(max_length=50, blank=True)
    display_title = models.BooleanField(default=True)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='None')
    order = models.PositiveIntegerField('Order', default=0)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lists')
    
    class Meta:
        ordering = ('order',)

    def __str__(self):
        return "{} ({})".format(self.title, self.module.title)

class ListItem(models.Model):
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=75, blank=True, null=True)
    caption = models.TextField(max_length=800, blank=True, null=True)
    order = models.PositiveIntegerField('Order', default=0)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='items')
    
    class Meta:
        verbose_name_plural = 'List items'
        ordering = ('order',)

    def __str__(self):
        return "{} ({})".format(self.title, self.list.title)


class Button(models.Model):
    caption = models.CharField(max_length=40, blank=False)
    url = models.URLField()

    def __str__(self):
        return "{}".format(self.caption)


class ButtonInModule(models.Model):
    button = models.ForeignKey(Button, on_delete=models.CASCADE, related_name='modules')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='buttons')
    order = models.PositiveIntegerField('Order', default=0)

    class Meta:
        ordering = ['order',]
        verbose_name = "Module"

    def __str__(self):
        return "{} ({})".format(self.button.caption, self.module.title)
    

class Post(models.Model):
    title = models.CharField(max_length=120, blank=False)
    slug = models.SlugField()
    public = models.BooleanField(default=True, help_text="If unchecked, only logged-in users can see this page")
    author = models.CharField(max_length=50, blank=False)
    date = models.DateField()
    image = FileBrowseField(max_length=200, directory="images/posts", format='Image', blank=True, null=True)
    content = HTMLField(max_length=65535, blank=False, null=True)
    excerpt = models.TextField(max_length=350, blank=False)
    categories = models.ManyToManyField('PostCategory', related_name='posts', blank=True)
    tags = TagField(get_absolute_url=lambda tag: reverse(
            'posts_by_tag', kwargs={'tag': tag.slug}
        ))
    
    class Meta:
        ordering = ['date', ]
    
    def __str__(self):
        return "{}, by {}".format(self.title, self.author)
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    

class ModuleInModule(models.Model):
    container = models.ForeignKey(ModuleContainer, null=False, on_delete=models.CASCADE, related_name='modulesinmodule')
    module = models.OneToOneField(Module, null=False, on_delete=models.CASCADE, related_name='containers')
    order = models.PositiveIntegerField('Order', default=0)
    
    class Meta:
        ordering = ['order',]
    
    def __str__(self):
        return "{} ({})".format(self.module.title, self.container.title)