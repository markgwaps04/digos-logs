# Generated by Django 3.0.7 on 2020-07-10 07:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TempPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=20)),
                ('last_name', models.CharField(default='', max_length=20)),
                ('middle_name', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('gender', models.IntegerField(choices=[(0, 'Male'), (1, 'Female')], default=0)),
                ('contact_number', models.BigIntegerField(default=0)),
                ('fullname', models.TextField(default='', max_length=20)),
            ],
            options={
                'db_table': 'vw_person',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Deparment',
            },
        ),
        migrations.CreateModel(
            name='In',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(0, 'In'), (1, 'In and Out')], default=0)),
                ('date', models.DateField(default=datetime.date.today)),
                ('time', models.TimeField(default=datetime.datetime.now)),
                ('purpose', models.TextField(blank=True, null=True)),
                ('contact_number', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'In',
                'verbose_name_plural': 'In',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=20)),
                ('last_name', models.CharField(default='', max_length=20)),
                ('middle_name', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('gender', models.IntegerField(choices=[(0, 'Male'), (1, 'Female')], default=0)),
                ('contact_number', models.BigIntegerField(default=0)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Out1',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('receiver_name', models.CharField(default='', max_length=20)),
                ('date_time', models.DateTimeField(default=datetime.date.today)),
                ('In', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.In')),
            ],
            options={
                'verbose_name': 'Out',
                'verbose_name_plural': 'Out',
            },
        ),
        migrations.AddField(
            model_name='in',
            name='person_visitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Person'),
        ),
    ]
