# Generated by Django 4.2 on 2024-05-28 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_inmueble_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='m2_totales',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
