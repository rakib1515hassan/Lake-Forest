from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

from apps.core.models import TimestampedModel, Image
from django.contrib.postgres.fields import ArrayField
from apps.events.models import Event

# Create your models here.
class FileSelection(models.Model):
    class FileType(models.TextChoices):
        URL = 'url'
        PDF = 'pdf'
    file_type = models.CharField(max_length = 3, choices = FileType.choices, default ='pdf')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']



class ResearchRepository(TimestampedModel):
    event = models.OneToOneField(
            Event, 
            on_delete=models.CASCADE, 
            related_name='research_repository'
        )

    title = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class HelpfulResources(FileSelection):
    research_repository = models.ForeignKey(
            ResearchRepository, 
            on_delete=models.CASCADE, 
            related_name='helpful_resources'
        )

    title = models.CharField(max_length=300)
    description = models.TextField()
    file = models.FileField(upload_to = "ResearchRepository/HelpfulResources", null=True, blank=True)
    url  = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.research_repository.title}, {self.title}"
    

class TaprootCauses(FileSelection):
    research_repository = models.ForeignKey(
            ResearchRepository, 
            on_delete=models.CASCADE,
            related_name='taproot_causes'
        )

    title = models.CharField(max_length=300)
    file  = models.FileField(upload_to = "ResearchRepository/TaprootCauses", null=True, blank=True)
    url   = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.research_repository.title}, {self.title}"
    


class ResponseStrategies(FileSelection):
    class StrategyTypes(models.TextChoices):
        DEFAULT  = 'default'
        CDC      = 'cdc'
        FIREARMS = 'firearms'
        DOMESTIC_VIOLENCE = 'domestic violence'

    research_repository = models.ForeignKey(
            ResearchRepository, 
            on_delete=models.CASCADE,
            related_name='response_strategies'
        )
    
    role = models.CharField(
        max_length = 30, 
        choices = StrategyTypes.choices,
        default ='default'
    )

    title = models.CharField(max_length=300)
    file  = models.FileField(upload_to = "ResearchRepository/TaprootCauses", null=True, blank=True)
    url   = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.research_repository.title}, {self.title}, Role = {self.role}"