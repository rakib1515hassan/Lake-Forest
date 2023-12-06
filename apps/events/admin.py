from django.contrib import admin
from apps.events.models import Event, EventsSchedule, EventsTeam, EventPanel

# Register your models here.
admin.site.register(Event)
admin.site.register(EventsSchedule)
admin.site.register(EventsTeam)
admin.site.register(EventPanel)
