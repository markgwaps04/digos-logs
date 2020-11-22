# Generated by Django 3.0.7 on 2020-08-20 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20200820_2346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document_type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=200)),
            ],
            options={
                'verbose_name': 'Type of documents',
                'verbose_name_plural': 'Type of documents',
            },
        ),
    ]