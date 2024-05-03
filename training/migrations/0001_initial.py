# Generated by Django 5.0.4 on 2024-05-03 05:50

import ckeditor_uploader.fields
import datetime
import django.db.models.deletion
import embed_video.fields
import image_cropping.fields
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
            name='TrainingCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Category Name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'training-category',
            },
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Description')),
                ('img1', models.ImageField(blank=True, null=True, upload_to='trainings/%Y/%m/%d/', verbose_name='Sidebar Image 1')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='trainings/%Y/%m/%d/', verbose_name='Sidebar Image 2')),
                ('img3', models.ImageField(blank=True, null=True, upload_to='trainings/%Y/%m/%d/', verbose_name='Sidebar Image 3')),
                ('img4', models.ImageField(blank=True, null=True, upload_to='trainings/%Y/%m/%d/', verbose_name='Sidebar Image 4')),
                ('cropped_img1', image_cropping.fields.ImageRatioField('img1', '345x230', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropped img1')),
                ('cropped_img2', image_cropping.fields.ImageRatioField('img2', '345x230', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropped img2')),
                ('cropped_img3', image_cropping.fields.ImageRatioField('img3', '345x230', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropped img3')),
                ('cropped_img4', image_cropping.fields.ImageRatioField('img4', '345x230', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropped img4')),
                ('trainer_name', models.CharField(max_length=200, null=True, verbose_name='Trainer Name')),
                ('email', models.EmailField(max_length=200, verbose_name='Email')),
                ('contact_no', models.CharField(max_length=15, verbose_name='Contact No')),
                ('video_url', embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name='Title Video')),
                ('video_url_1', embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name='Sidebar Video 1')),
                ('video_url_2', embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name='Sidebar Video 2')),
                ('video_url_3', embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name='Sidebar Video 3')),
                ('video_url_4', embed_video.fields.EmbedVideoField(blank=True, null=True, verbose_name='Sidebar Video 4')),
                ('location', models.CharField(blank=True, max_length=200, null=True, verbose_name='Venue Details')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, editable=False, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('views', models.IntegerField(default=0, verbose_name='Views')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('city', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='state', chained_model_field='state', null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='settings.country')),
                ('state', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='country', chained_model_field='country', null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.state')),
                ('category_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.trainingcategory')),
            ],
            options={
                'verbose_name': 'Training',
                'verbose_name_plural': 'Trainings',
                'db_table': 'training',
            },
        ),
    ]
