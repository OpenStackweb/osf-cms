# Generated by Django 2.0.1 on 2018-02-20 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0005_socialmediamenu'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialmediamenu',
            options={'ordering': ['order'], 'verbose_name': 'Social Media Menu', 'verbose_name_plural': 'Social Media Menu'},
        ),
        migrations.RemoveField(
            model_name='bigheadermenu',
            name='event',
        ),
        migrations.RemoveField(
            model_name='footermenu',
            name='event',
        ),
        migrations.RemoveField(
            model_name='socialmediamenu',
            name='event',
        ),
    ]