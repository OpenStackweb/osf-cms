# Generated by Django 2.0.1 on 2018-01-17 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0032_auto_20180117_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitem',
            name='style',
            field=models.CharField(choices=[('NONE', 'None'), ('VERTICALSEP', 'Vertical separators'), ('HORIZONTALSEP', 'Horizontal separator on top')], default='None', max_length=6),
        ),
    ]