# Generated by Django 3.0.6 on 2020-05-09 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_remove_publication_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publication',
            old_name='datetime',
            new_name='date',
        ),
    ]
