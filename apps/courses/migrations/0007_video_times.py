# Generated by Django 2.1 on 2018-09-05 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='times',
            field=models.IntegerField(default=0, verbose_name='视频时长（分钟数）'),
        ),
    ]