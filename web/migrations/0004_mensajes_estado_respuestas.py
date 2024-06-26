# Generated by Django 4.2 on 2024-05-24 04:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_rename_contactos_mensajes'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensajes',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('leido', 'Leido'), ('respondido', 'Respondido')], default='pendiente', max_length=20),
        ),
        migrations.CreateModel(
            name='Respuestas',
            fields=[
                ('id_respuesta', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('respuesta', models.TextField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('mensaje_padre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.mensajes')),
            ],
        ),
    ]
