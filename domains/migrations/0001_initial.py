# Generated by Django 2.0.1 on 2018-03-14 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedirectHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redirect_name', models.CharField(max_length=50)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redirect_hosts', to='sites.Site')),
            ],
        ),
    ]
