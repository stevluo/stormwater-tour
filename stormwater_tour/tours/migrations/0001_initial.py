# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='InfoTab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='InfoTabElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='InfoTabElementImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('file_location', models.FileField(upload_to='static/tours/images/')),
            ],
        ),
        migrations.CreateModel(
            name='LandingPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MapLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=8)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='MapPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('map_default_zoom', models.PositiveSmallIntegerField()),
                ('map_min_zoom', models.PositiveSmallIntegerField()),
                ('map_max_zoom', models.PositiveSmallIntegerField()),
                ('current_site_map_marker', models.FileField(upload_to='static/tours/images/')),
                ('next_site_map_marker', models.FileField(upload_to='static/tours/images/')),
                ('site_visited_map_marker', models.FileField(upload_to='static/tours/images/')),
                ('site_unvisited_map_marker', models.FileField(upload_to='static/tours/images/')),
                ('map_center', models.OneToOneField(to='tours.MapLocation', related_name='map_center')),
                ('map_lower_bound', models.OneToOneField(to='tours.MapLocation', related_name='map_lower_bound')),
                ('map_upper_bound', models.OneToOneField(to='tours.MapLocation', related_name='map_upper_bound')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('site_slug', models.SlugField()),
                ('simple_directions', models.TextField()),
                ('site_type', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('tour_order', models.PositiveSmallIntegerField()),
                ('location', models.OneToOneField(to='tours.MapLocation')),
            ],
        ),
        migrations.CreateModel(
            name='SiteImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('file_location', models.FileField(upload_to='static/tours/images/')),
                ('site', models.ForeignKey(to='tours.Site')),
            ],
        ),
        migrations.CreateModel(
            name='ThankYouPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('tour_slug', models.SlugField(unique=True)),
                ('site_nickname', models.CharField(max_length=100)),
                ('travel_method', models.CharField(choices=[('DRIVING', 'DRIVING'), ('WALKING', 'WALKING'), ('BICYCLING', 'BICYCLING'), ('TRANSIT', 'TRANSIT')], max_length=9)),
                ('about_page', models.OneToOneField(to='tours.AboutPage')),
                ('feedback_page', models.OneToOneField(to='tours.FeedbackPage')),
                ('landing_page', models.OneToOneField(to='tours.LandingPage')),
                ('map_page', models.OneToOneField(to='tours.MapPage')),
            ],
        ),
        migrations.CreateModel(
            name='UserFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('origin', models.CharField(blank=True, choices=[('Northern California', 'Northern California'), ('Southern California', 'Southern California'), ('Outside of California', 'Outside of California')], max_length=100)),
                ('reason', models.TextField(blank=True, max_length=500)),
                ('feedback', models.TextField(blank=True, max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'user feedback',
            },
        ),
        migrations.AddField(
            model_name='site',
            name='tour',
            field=models.ForeignKey(to='tours.Tour'),
        ),
        migrations.AddField(
            model_name='infotabelement',
            name='image',
            field=models.OneToOneField(to='tours.InfoTabElementImage'),
        ),
        migrations.AddField(
            model_name='infotab',
            name='elements',
            field=models.ManyToManyField(to='tours.InfoTabElement'),
        ),
        migrations.AddField(
            model_name='infotab',
            name='site',
            field=models.ForeignKey(to='tours.Site'),
        ),
        migrations.AddField(
            model_name='feedbackpage',
            name='thank_you_page',
            field=models.OneToOneField(to='tours.ThankYouPage'),
        ),
        migrations.AddField(
            model_name='aboutelement',
            name='about_page',
            field=models.ForeignKey(to='tours.AboutPage'),
        ),
        migrations.AlterUniqueTogether(
            name='site',
            unique_together=set([('tour', 'title'), ('tour', 'site_slug'), ('tour', 'tour_order')]),
        ),
        migrations.AlterUniqueTogether(
            name='infotab',
            unique_together=set([('site', 'title')]),
        ),
    ]
