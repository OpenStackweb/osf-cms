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