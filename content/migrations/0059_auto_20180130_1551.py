# Generated by Django 2.0.1 on 2018-01-30 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0058_auto_20180130_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='email',
            field=models.EmailField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='speaker',
            name='workplace',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]