# Generated by Django 4.2.7 on 2023-12-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_eventsteam_team_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
