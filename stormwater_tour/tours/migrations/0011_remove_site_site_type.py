# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0010_mapbuildingmarker_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='site_type',
        ),
    ]
