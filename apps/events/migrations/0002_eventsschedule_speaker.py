# Generated by Django 4.2.7 on 2023-12-04 11:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsschedule',
            name='speaker',
            field=models.ManyToManyField(related_name='schedule_speaker', to=settings.AUTH_USER_MODEL),
        ),
    ]
