# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfeedback',
            name='reason',
        ),
        migrations.AddField(
            model_name='userfeedback',
            name='background',
            field=models.CharField(choices=[('Student', 'Student'), ('Industry Professional', 'Industry Professional'), ('General Public', 'General Public')], blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='origin',
            field=models.CharField(choices=[('Local (Sacramento and its neighboring counties)', 'Local (Sacramento and its neighboring counties)'), ('Northern California', 'Northern California'), ('Southern California', 'Southern California'), ('Outside of California', 'Outside of California')], blank=True, max_length=100),
        ),
    ]
