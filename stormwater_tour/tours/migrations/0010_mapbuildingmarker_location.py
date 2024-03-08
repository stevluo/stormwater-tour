# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0009_mapbuildingmarker'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapbuildingmarker',
            name='location',
            field=models.OneToOneField(null=True, to='tours.MapLocation'),
        ),
    ]
