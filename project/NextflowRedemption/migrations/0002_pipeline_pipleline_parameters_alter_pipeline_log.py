# Generated by Django 4.1.2 on 2022-11-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NextflowRedemption', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipeline',
            name='pipleline_parameters',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='log',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
