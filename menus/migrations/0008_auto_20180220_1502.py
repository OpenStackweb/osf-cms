# Generated by Django 2.0.1 on 2018-02-20 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0007_auto_20180220_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialmediamenu',
            name='url',
            field=models.CharField(max_length=200),
        ),
    ]
