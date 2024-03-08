# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0003_auto_20160229_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infotab',
            name='elements',
            field=models.ManyToManyField(to='tours.InfoTabElement', blank=True),
        ),
        migrations.AlterField(
            model_name='mappage',
            name='current_site_marker',
            field=models.FileField(upload_to='static/tours/map_markers/', null=True, help_text='Suggested image size: 32px x 32px', blank=True),
        ),
        migrations.AlterField(
            model_name='mappage',
            name='next_site_marker',
            field=models.FileField(upload_to='static/tours/map_markers/', null=True, help_text='Suggested image size: 32px x 32px', blank=True),
        ),
        migrations.AlterField(
            model_name='mappage',
            name='site_unvisited_marker',
            field=models.FileField(upload_to='static/tours/map_markers/', null=True, help_text='Suggested image size: 32px x 32px', blank=True),
        ),
        migrations.AlterField(
            model_name='mappage',
            name='site_visited_marker',
            field=models.FileField(upload_to='static/tours/map_markers/', null=True, help_text='Suggested image size: 32px x 32px', blank=True),
        ),
    ]
