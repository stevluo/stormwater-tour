# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0006_auto_20160320_0147'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeedback',
            name='method',
            field=models.CharField(choices=[('I physically travelled between sites', 'I physically travelled between sites'), ('I did not visit more than one physical installation', 'I did not visit more than one physical installation')], max_length=100, blank=True),
        ),
    ]
