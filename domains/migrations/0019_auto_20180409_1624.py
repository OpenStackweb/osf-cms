# Generated by Django 2.0.1 on 2018-04-09 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0018_auto_20180403_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redirecthost',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='redirect_hosts', to='sites.Site'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='home_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.Page'),
        ),
    ]