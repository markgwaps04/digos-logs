# Generated by Django 3.0.7 on 2020-08-19 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='A',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='childB',
            fields=[
                ('a_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='home.A')),
                ('idA', models.AutoField(primary_key=True, serialize=False)),
                ('nameB', models.CharField(default='', max_length=100)),
            ],
            bases=('home.a',),
        ),
        migrations.CreateModel(
            name='childC',
            fields=[
                ('a_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='home.A')),
                ('idC', models.AutoField(primary_key=True, serialize=False)),
                ('nameC', models.CharField(default='', max_length=100)),
            ],
            bases=('home.a',),
        ),
    ]
