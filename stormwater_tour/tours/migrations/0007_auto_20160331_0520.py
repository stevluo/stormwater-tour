# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0006_auto_20160320_0147'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingMarkerImage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file_location', models.FileField(upload_to='tours/images/')),
                ('building_location', models.OneToOneField(related_name='building_location', to='tours.MapLocation')),
            ],
        ),
        migrations.AddField(
            model_name='mappage',
            name='building_marker',
            field=models.ManyToManyField(blank=True, to='tours.BuildingMarkerImage'),
        ),
    ]
