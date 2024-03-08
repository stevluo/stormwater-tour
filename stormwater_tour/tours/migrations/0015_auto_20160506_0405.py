# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0014_auto_20160506_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='serve_as_html',
            field=models.BooleanField(default=False, help_text='Enables full html use in text fields. Affects: Description.'),
        ),
    ]
