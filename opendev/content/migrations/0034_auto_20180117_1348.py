# Generated by Django 2.0.1 on 2018-01-17 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0033_listitem_style'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listitem',
            name='style',
        ),
        migrations.AddField(
            model_name='block',
            name='list_style',
            field=models.CharField(choices=[('NONE', 'None'), ('VERTICALSEP', 'Vertical separators'), ('HORIZONTALSEP', 'Horizontal separator on top')], default='None', max_length=6),
        ),
        migrations.AddField(
            model_name='listitem',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]