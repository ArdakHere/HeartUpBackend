# Generated by Django 5.0.3 on 2024-05-04 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0021_doctor_first_name_doctor_height_doctor_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='height',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='weight',
        ),
        migrations.AddField(
            model_name='patient',
            name='height',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.FloatField(null=True),
        ),
    ]
