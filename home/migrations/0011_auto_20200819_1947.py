# Generated by Django 3.0.7 on 2020-08-19 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20200819_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='home.A'),
        ),
    ]
