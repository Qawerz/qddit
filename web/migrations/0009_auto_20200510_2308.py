# Generated by Django 3.0.6 on 2020-05-10 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20200510_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='date',
        ),
        migrations.AddField(
            model_name='publication',
            name='create_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
