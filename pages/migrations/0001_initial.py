# Generated by Django 5.0.4 on 2024-05-03 05:50

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, null=True, unique=True, verbose_name='Title')),
                ('slug', models.SlugField(max_length=500, unique=True, verbose_name='Slug')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Description')),
                ('image', models.ImageField(help_text='326x244', null=True, upload_to='diary/%Y/%m/%d/', verbose_name='Image')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('views', models.IntegerField(default=0, verbose_name='Views')),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft')], default='Published', max_length=15, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Dairy',
                'verbose_name_plural': 'Dairies',
                'db_table': 'pages-diary',
            },
        ),
        migrations.CreateModel(
            name='generalResearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, unique=True, verbose_name='Title')),
                ('slug', models.SlugField(max_length=500, unique=True, verbose_name='Slug')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='general/research/%Y/%m/%d/', verbose_name='Image')),
                ('views', models.IntegerField(default=0, verbose_name='Views')),
                ('meta_title', models.CharField(max_length=60, null=True, verbose_name='Meta Title')),
                ('meta_description', models.CharField(max_length=158, null=True, verbose_name='Meta Description')),
                ('meta_keywords', models.CharField(help_text='Word separated by commas', max_length=500, null=True, verbose_name='Meta Keywords')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft')], default='Published', max_length=15, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Research Articles on LY',
                'verbose_name_plural': 'Research Articles on LY',
                'db_table': 'pages-research-list',
            },
        ),
        migrations.CreateModel(
            name='GetInvolved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Title')),
                ('description', models.CharField(max_length=255, null=True, verbose_name='Description')),
                ('image', models.ImageField(upload_to='getinvolved/%Y/%m/%d/', verbose_name='Image')),
                ('btn_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Button Name')),
                ('url', models.URLField(verbose_name='Link URL')),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft')], default='Published', max_length=15, verbose_name='Status')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
            ],
            options={
                'verbose_name': 'Get Involved',
                'verbose_name_plural': 'Get Involved',
                'db_table': 'pages-get-involved',
            },
        ),
        migrations.CreateModel(
            name='laughterBlogsCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
            ],
            options={
                'verbose_name': 'Laughter Blog Category',
                'verbose_name_plural': 'Laughter Blog Category',
                'db_table': 'pages-laughter-blog-category-list',
            },
        ),
        migrations.CreateModel(
            name='laughterBlogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, unique=True, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, null=True, unique=True, verbose_name='Slug')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Description')),
                ('image', models.ImageField(upload_to='laughterBlogs/%Y/%m/%d/', verbose_name='Image')),
                ('views', models.IntegerField(blank=True, default=0, null=True, verbose_name='Views')),
                ('meta_title', models.CharField(max_length=60, null=True, verbose_name='Meta Title')),
                ('meta_description', models.CharField(max_length=158, null=True, verbose_name='Meta Description')),
                ('meta_keywords', models.CharField(help_text='Word separated by commas', max_length=500, null=True, verbose_name='Meta Keywords')),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft')], default='Published', max_length=15, verbose_name='Status')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.laughterblogscat')),
            ],
            options={
                'verbose_name': 'Laughter Blog',
                'verbose_name_plural': 'Laughter Blogs',
                'db_table': 'pages-laughter-blog-list',
            },
        ),
    ]