# Generated by Django 4.2.7 on 2023-12-07 05:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0012_event_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsteam',
            name='member',
            field=models.ManyToManyField(related_name='team_members', to=settings.AUTH_USER_MODEL),
        ),
    ]
