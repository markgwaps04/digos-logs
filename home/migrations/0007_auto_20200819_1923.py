# Generated by Django 3.0.7 on 2020-08-19 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20200819_1921'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gago',
            old_name='request_id',
            new_name='id',
        ),
    ]