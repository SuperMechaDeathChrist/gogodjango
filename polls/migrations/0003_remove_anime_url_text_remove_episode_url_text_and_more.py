# Generated by Django 4.0.6 on 2022-07-15 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_rename_url_episode_url_text_anime_url_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime',
            name='url_text',
        ),
        migrations.RemoveField(
            model_name='episode',
            name='url_text',
        ),
        migrations.AddField(
            model_name='anime',
            name='url',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='episode',
            name='url',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='episode',
            name='stream_url',
            field=models.CharField(default='', max_length=200),
        ),
    ]
