# Generated by Django 4.0.3 on 2022-04-06 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('concursoApp', '0003_pregunta_max_puntaje_alter_elegirrespuesta_pregunta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntasrespondida',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intentos', to='concursoApp.quizusuario'),
        ),
    ]
