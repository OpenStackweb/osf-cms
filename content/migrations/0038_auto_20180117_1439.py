# Generated by Django 2.0.1 on 2018-01-17 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0037_auto_20180117_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='content_width',
            field=models.CharField(choices=[('WIDE', 'Wide'), ('SEMIWIDE', 'Semiwide'), ('NARROW', 'Narrow')], default='WIDE', max_length=6),
        ),
    ]