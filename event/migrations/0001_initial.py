# Generated by Django 5.0.4 on 2024-05-03 05:50

import ckeditor_uploader.fields
import datetime
import django.db.models.deletion
import embed_video.fields
import smart_selects.db_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('settings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='worldLaughterDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Banner', 'Banner'), ('Blue Background Logo', 'Blue Background Logo'), ('Message', 'Message'), ('Round Logo', 'Round Logo')], default='Banner', max_length=200, verbose_name='Category')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('image', models.ImageField(null=True, upload_to='wld/jpg/%Y/%m/%d/', verbose_name='Image URL')),
                ('pdf', models.FileField(null=True, upload_to='wld/pdf/%Y/%m/%d/', verbose_name='PDF URL')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, editable=False, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
            ],
            options={
                'verbose_name': 'WLD',
                'verbose_name_plural': 'WLD',
                'db_table': 'world-laughter-day',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Free Public Seminar', 'Free Public Seminar'), ('Workshop', 'Workshop'), ('Conference', 'Conference'), ('World Laughter Day', 'World Laughter Day')], default='free', max_length=30, verbose_name='Category')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Description')),
                ('organiser_name', models.CharField(max_length=200, verbose_name='Organiser Name')),
                ('email', models.EmailField(max_length=200, verbose_name='Email')),
                ('contact_no', models.CharField(blank=True, max_length=15, null=True, verbose_name='Contact No')),
                ('location', models.CharField(max_length=200, verbose_name='Location')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('website_url', models.URLField(blank=True, null=True, verbose_name='Website URL')),
                ('img1', models.ImageField(blank=True, null=True, upload_to='events/%Y/%m/%d/', verbose_name='Event Image 1')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='events/%Y/%m/%d/', verbose_name='Event Image 2')),
                ('video1', embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name='Event Video 1')),
                ('video2', embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name='Event Video 2')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, editable=False, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('views', models.IntegerField(default=0, verbose_name='Views')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('city', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='state', chained_model_field='state', null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='settings.country')),
                ('state', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='country', chained_model_field='country', null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.state')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'db_table': 'events',
            },
        ),
    ]
