# Generated by Django 3.1.7 on 2021-05-15 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0008_auto_20210515_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registro',
            name='test',
        ),
        migrations.RemoveField(
            model_name='resultado',
            name='registro',
        ),
    ]
