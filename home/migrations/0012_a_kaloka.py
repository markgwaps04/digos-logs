# Generated by Django 3.0.7 on 2020-08-19 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20200819_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='a',
            name='kaloka',
            field=models.CharField(default='gaga', max_length=100),
        ),
    ]