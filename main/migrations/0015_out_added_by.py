# Generated by Django 3.0.7 on 2020-07-15 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200715_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='out',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.UserProfile'),
        ),
    ]
