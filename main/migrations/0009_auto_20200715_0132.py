# Generated by Django 3.0.7 on 2020-07-14 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200715_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='out',
            name='In',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.In'),
        ),
    ]
