# Generated by Django 3.0.6 on 2020-05-10 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20200510_0230'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=30)),
                ('date', models.CharField(max_length=120)),
                ('text', models.TextField()),
            ],
        ),
    ]
