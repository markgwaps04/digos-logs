# Generated by Django 3.0.7 on 2020-08-20 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='in',
            name='type',
            field=models.IntegerField(choices=[(0, 'In'), (1, 'Out'), (2, 'In and Out')], default=0),
        ),
        migrations.DeleteModel(
            name='Log',
        ),
    ]
