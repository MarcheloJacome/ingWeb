# Generated by Django 3.1.7 on 2021-05-17 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0009_auto_20210515_1603'),
        ('resultados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultado',
            name='registro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='principal.registro'),
        ),
    ]
