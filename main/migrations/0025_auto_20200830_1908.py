# Generated by Django 3.0.7 on 2020-08-30 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20200830_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log_details',
            name='document_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Document_type'),
        ),
    ]
