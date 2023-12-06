# Generated by Django 4.2.7 on 2023-12-05 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0002_eventsschedule_speaker'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchRepository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='research_repository', to='events.event')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaprootCauses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=300)),
                ('file', models.FileField(blank=True, null=True, upload_to='ResearchRepository/TaprootCauses')),
                ('url', models.URLField(blank=True, null=True)),
                ('research_repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taproot_causes', to='repositorys.researchrepository')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResponseStrategies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(choices=[('default', 'Default'), ('cdc', 'Cdc'), ('firearms', 'Firearms'), ('domestic violence', 'Domestic Violence')], default='default', max_length=30)),
                ('title', models.CharField(max_length=300)),
                ('file', models.FileField(blank=True, null=True, upload_to='ResearchRepository/TaprootCauses')),
                ('url', models.URLField(blank=True, null=True)),
                ('research_repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='response_strategies', to='repositorys.researchrepository')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HelpfulResources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to='ResearchRepository/HelpfulResources')),
                ('url', models.URLField(blank=True, null=True)),
                ('research_repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='helpful_resources', to='repositorys.researchrepository')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]
