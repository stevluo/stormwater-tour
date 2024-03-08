# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mappage',
            name='current_site_map_marker',
        ),
        migrations.RemoveField(
            model_name='mappage',
            name='next_site_map_marker',
        ),
        migrations.RemoveField(
            model_name='mappage',
            name='site_unvisited_map_marker',
        ),
        migrations.RemoveField(
            model_name='mappage',
            name='site_visited_map_marker',
        ),
        migrations.AddField(
            model_name='feedbackpage',
            name='feedback_request_checkpoint',
            field=models.PositiveSmallIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='mappage',
            name='current_site_marker',
            field=models.FileField(null=True, upload_to='static/tours/map_markers/'),
        ),
        migrations.AddField(
            model_name='mappage',
            name='next_site_marker',
            field=models.FileField(null=True, upload_to='static/tours/map_markers/'),
        ),
        migrations.AddField(
            model_name='mappage',
            name='site_unvisited_marker',
            field=models.FileField(null=True, upload_to='static/tours/map_markers/'),
        ),
        migrations.AddField(
            model_name='mappage',
            name='site_visited_marker',
            field=models.FileField(null=True, upload_to='static/tours/map_markers/'),
        ),
    ]
