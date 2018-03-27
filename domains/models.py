from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class BaseSiteModel(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='%(class)ss')

    class Meta:
        abstract = True


class RedirectHost(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='redirect_hosts')
    redirect_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return "{} {}".format(self.redirect_name, self.site.name)


class SiteSettings(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='settings')
    custom_css = models.TextField(blank=True, null=True, verbose_name='Custom CSS')
    custom_js = models.TextField(blank=True, null=True, verbose_name='Custom JS',
                                 help_text="Printed just before the closing </head> tag. Make sure it's an async script. It will be rendered as-is, unescaped, so make sure its coming from a trusted source.")
    home_page = models.ForeignKey('content.Page', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'Site'


@receiver(post_save, sender=Site)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        SiteSettings.objects.create(site=instance)
