# Generated by Django 2.0.1 on 2018-03-28 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0008_auto_20180328_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='base_site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cloned_site_settings', to='sites.Site', verbose_name='Clone from'),
        ),
    ]
