# Generated by Django 2.0.1 on 2018-01-17 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0044_auto_20180117_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buttoninmodule',
            name='button',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buttons', to='content.Button'),
        ),
        migrations.AlterField(
            model_name='buttoninmodule',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='content.Module'),
        ),
    ]
