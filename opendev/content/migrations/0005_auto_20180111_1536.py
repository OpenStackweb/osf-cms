# Generated by Django 2.0.1 on 2018-01-11 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_module_image_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('module_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.Module')),
                ('layout', models.CharField(choices=[('ONECOL', 'One column'), ('TWOCOL', 'Two columns')], default='ONECOL', max_length=6)),
            ],
            bases=('content.module',),
        ),
        migrations.AddField(
            model_name='module',
            name='kicker',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='module',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='sponsorship',
            name='subtitle',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='talk',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
