# Generated by Django 3.0.7 on 2020-09-28 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_log_details_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='is_out',
            field=models.BooleanField(default=False),
        ),
    ]
