from django.core.exceptions import ValidationError
from django.db import models

from content.models import Page

# TOFIX implement Sites instead of models.Model
from domains.models import BaseSiteModel


class Menu(BaseSiteModel):
    display_name = models.CharField('Label', max_length=255)
    target_type = models.CharField('Link target', max_length=255, choices=[
        ('page', 'Page (select a page below)'), ('url', 'URL (enter one below)')], default='url')
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.SET_NULL)
    url = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def clean(self):
        if self.target_type == 'page' and not self.page:
            raise ValidationError({'page': 'Please select a target page.'})
        if self.target_type == 'url' and not self.url:
            raise ValidationError({'url': 'Please enter a target URL.'})

    def __str__(self):
        return self.display_name

    class Meta:
        ordering = ['order']
        abstract = True


class BigHeaderMenu(Menu):

    class Meta(Menu.Meta):
        verbose_name = verbose_name_plural = 'Main Menu'


class SocialMediaMenu(Menu):
    NETWORKS = (
        ('fa-twitter', 'Twitter'),
        ('fa-github', 'GitHub'),
        ('fa-slack', 'Slack'),
        ('fa-youtube', 'Youtube'),
        ('fa-facebook', 'Facebook'),
    )

    url = models.CharField(max_length=200, blank=False)

    social_network = models.CharField(max_length=25, blank=False, choices=NETWORKS)

    class Meta(Menu.Meta):
        verbose_name = verbose_name_plural = 'Social Media Menu'


class FooterMenu(Menu):

    class Meta(Menu.Meta):
        verbose_name = verbose_name_plural = 'Footer Menu'
