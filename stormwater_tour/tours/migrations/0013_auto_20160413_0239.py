# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 02:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0012_merge'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MapBuildingMarker',
            new_name='MapLandmarkMarker',
        ),
        migrations.AlterField(
            model_name='infotabelement',
            name='image',
            field=models.FileField(upload_to='tours/images/'),
        ),
        migrations.DeleteModel(
            name='InfoTabElementImage',
        ),
    ]
