# Generated by Django 4.2.7 on 2023-12-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_remove_eventsschedule_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="analysis_rubric",
            field=models.FileField(blank=True, null=True, upload_to="analysis_rubric"),
        ),
    ]
