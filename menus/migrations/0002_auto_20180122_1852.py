# Generated by Django 2.0.1 on 2018-01-22 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bigheadermenu',
            name='url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='footermenu',
            name='url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
