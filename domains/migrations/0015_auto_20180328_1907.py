# Generated by Django 2.0.1 on 2018-03-28 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0014_auto_20180328_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='base_site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clone_settings', to='domains.SiteSettings', verbose_name='Clone from'),
        ),
    ]
