# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0007_auto_20160331_0520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildingmarkerimage',
            name='building_location',
        ),
        migrations.RemoveField(
            model_name='mappage',
            name='building_marker',
        ),
        migrations.DeleteModel(
            name='BuildingMarkerImage',
        ),
    ]
