# Generated by Django 3.0.6 on 2020-05-31 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_auto_20200531_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='votes',
        ),
        migrations.AddField(
            model_name='comments',
            name='karma',
            field=models.IntegerField(default=0, verbose_name='Популярность комментария'),
        ),
        migrations.AddField(
            model_name='publication',
            name='karma',
            field=models.IntegerField(default=0, verbose_name='Популярность статьи'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Видемость статьи'),
        ),
    ]