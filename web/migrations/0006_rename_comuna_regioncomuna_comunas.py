# Generated by Django 4.2 on 2024-05-27 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_regioncomuna'),
    ]

    operations = [
        migrations.RenameField(
            model_name='regioncomuna',
            old_name='comuna',
            new_name='comunas',
        ),
    ]
