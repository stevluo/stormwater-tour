# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-05 05:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0014_tour_tour_css'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='tour_css',
            field=models.FileField(blank=True, help_text='When used adds the uploaded css file to every page of the tour.', null=True, upload_to='tours/css/'),
        ),
    ]
