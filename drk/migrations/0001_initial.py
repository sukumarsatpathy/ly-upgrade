# Generated by Django 5.0.4 on 2024-05-03 05:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UpcomingEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('startDate', models.DateTimeField(null=True, verbose_name='Start Date')),
                ('duration', models.CharField(max_length=100, null=True, verbose_name='Duration')),
                ('timing', models.CharField(max_length=100, null=True, verbose_name='Timing')),
                ('language', models.CharField(max_length=100, null=True, verbose_name='Language')),
                ('btnText', models.CharField(max_length=50, null=True, verbose_name='Button Text')),
                ('btnURL', models.URLField(null=True, verbose_name='Button URL')),
                ('btnBgColor', models.CharField(max_length=50, null=True, verbose_name='Button Color')),
                ('image', models.ImageField(null=True, upload_to='upcomingEvents/%Y/%m/%d/', verbose_name='Image')),
                ('is_daily', models.BooleanField(default=False, verbose_name='Is Daily?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
            ],
            options={
                'verbose_name': 'Upcoming Event',
                'verbose_name_plural': 'Upcoming Events',
                'db_table': 'drk_upcoming_events',
            },
        ),
    ]
