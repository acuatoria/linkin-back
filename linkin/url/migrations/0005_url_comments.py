# Generated by Django 4.0.4 on 2022-11-01 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url', '0004_remove_url_show_on_front_url_hide_from_public_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='comments',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
