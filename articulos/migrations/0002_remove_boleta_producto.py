# Generated by Django 5.0.6 on 2024-07-12 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articulos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boleta',
            name='producto',
        ),
    ]