# Generated by Django 3.0.7 on 2020-07-15 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20200715_0134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='out',
            name='time',
        ),
    ]
