from django.contrib.sites.models import Site
from django.db import migrations

from content.models import Page
from domains.models import CustomSite


def gen_customsites(apps, schema_editor):
    sites = Site.objects.all()
    for site in sites:
        home_page = Page.objects.filter(site=site, slug='').first()
        if home_page:
            CustomSite.objects.get_or_create(site=site, home_page=home_page, custom_js=None)
        else:
            CustomSite.objects.get_or_create(site=site, home_page=None, custom_js=None)



class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0002_customsite'),
    ]

    operations = [
        migrations.RunPython(gen_customsites)
    ]
