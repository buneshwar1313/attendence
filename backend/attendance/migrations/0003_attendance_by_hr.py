# Generated by Django 4.2.1 on 2023-06-04 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_attendance_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='By_hr',
            field=models.BooleanField(default=False),
        ),
    ]
