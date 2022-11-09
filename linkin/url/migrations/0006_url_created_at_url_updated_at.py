# Generated by Django 4.0.4 on 2022-11-06 19:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('url', '0005_url_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='url',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
