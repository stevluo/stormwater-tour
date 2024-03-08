# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0008_auto_20160331_0527'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapBuildingMarker',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('file_location', models.FileField(upload_to='tours/images/')),
                ('map_page', models.ForeignKey(to='tours.MapPage')),
            ],
        ),
    ]
