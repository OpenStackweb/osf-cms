import git
import os

import re
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from git import GitCommandError

from domains.clone_site import CloneViewSet


class BaseSiteModel(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='%(class)ss')

    class Meta:
        abstract = True


class RedirectHost(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='redirect_hosts', null=True)
    redirect_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return "{} --> {}".format(self.redirect_name, self.site.name)


class SiteSettings(models.Model):
    base_site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Clone from', related_name='clone_settings')
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='settings')
    custom_css = models.TextField(blank=True, null=True, verbose_name='Custom CSS')
    custom_js = models.TextField(blank=True, null=True, verbose_name='Custom JS',
                                 help_text="Printed just before the closing </head> tag. Make sure it's an async script. It will be rendered as-is, unescaped, so make sure its coming from a trusted source.")
    home_page = models.ForeignKey('content.Page', on_delete=models.SET_NULL, null=True)
    remote_url = models.URLField()
    
    def __init__(self, *args, **kwargs):
        super(SiteSettings, self).__init__(*args, **kwargs)
        self.initial_remote_url = self.remote_url
    
    def __str__(self):
        return '{} settings'.format(self.site.name)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'


@receiver(post_save, sender=SiteSettings)
def clone_site(sender, **kwargs):
    if kwargs['created'] and kwargs['instance'].base_site:
        cvs = CloneViewSet(kwargs['instance'].base_site, kwargs['instance'].site)
        home_page = cvs.main()
        kwargs['instance'].home_page_id = home_page
        kwargs['instance'].save()


@receiver(pre_save, sender=SiteSettings)
def setup_remote_repo(sender, instance, **kwargs):
    if instance.initial_remote_url != instance.remote_url:
        submodule_name = re.match(r"((git@|https://|http://)([\w.@]+)(/|:))([\w,\-_]+)/([\w,\-_]+)(.git){0,1}((/){0,1})",
                                  instance.site.settings.remote_url).group(6)
        repo = git.Repo('.git')
        try:
            repo.create_submodule(name=submodule_name,path=os.path.join(settings.STATIC_ROOT, submodule_name),
                              url=instance.remote_url)
            repo.index.commit(message='Added submodule {}'.format(submodule_name))
        except GitCommandError:
            raise ValidationError('Please insert a correct git repository url')
    
    # submodules = repo.submodules
