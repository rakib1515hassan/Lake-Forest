from django.contrib import admin
from apps.repositorys.models import (
    ResearchRepository,
    HelpfulResources,
    TaprootCauses,
    ResponseStrategies,
    ImpactOnSociety,
)


# Register your models here.
admin.site.register(ResearchRepository)
admin.site.register(HelpfulResources)
admin.site.register(TaprootCauses)
admin.site.register(ResponseStrategies)
admin.site.register(ImpactOnSociety)
