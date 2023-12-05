from django.contrib import admin
from apps.repositorys.models import (
    ResearchRepository,
    HelpfulResources,
    TaprootCauses,
    ResponseStrategies
)


# Register your models here.
admin.site.register(ResearchRepository)
admin.site.register(HelpfulResources)
admin.site.register(TaprootCauses)
admin.site.register(ResponseStrategies)