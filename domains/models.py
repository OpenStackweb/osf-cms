from django.contrib.sites.models import Site
from django.db import models


class BaseSiteModel(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='%(class)ss')
    
    class Meta:
        abstract = True


class RedirectHost(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='redirect_hosts')
    redirect_name = models.CharField(max_length=50, blank=False)
    
    def __str__(self):
        return "{} {}".format(self.redirect_name, self.site.name)
    

class CustomSite(Site):
    custom_js = models.TextField(blank=True, null=True, verbose_name='Custom JS', help_text="Printed just before the closing </head> tag. Make sure it's an async script. It will be rendered as-is, unescaped, so make sure its coming from a trusted source.")

    class Meta:
        verbose_name = 'Site'