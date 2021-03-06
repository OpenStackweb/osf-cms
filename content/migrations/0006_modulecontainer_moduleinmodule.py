# Generated by Django 2.0.1 on 2018-02-28 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20180227_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleContainer',
            fields=[
                ('module_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.Module')),
            ],
            options={
                'verbose_name_plural': 'Module containers',
            },
            bases=('content.module',),
        ),
        migrations.CreateModel(
            name='ModuleInModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modulesinmodule', to='content.ModuleContainer')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='containers', to='content.Module')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
