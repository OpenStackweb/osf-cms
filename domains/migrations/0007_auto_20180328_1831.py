# Generated by Django 2.0.1 on 2018-03-28 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0006_auto_20180328_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='sites.Site'),
        ),
    ]
