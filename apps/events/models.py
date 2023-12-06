from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

from apps.core.models import TimestampedModel, Image
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Event(TimestampedModel):
    title = models.CharField(max_length=225)

    banner_image = models.ImageField(upload_to="Event/Banner", null=True, blank=True)
    screen_image = models.ImageField(
        upload_to="Event/ScreenImage", null=True, blank=True
    )

    register_team_date = models.DateField()
    select_topic_date  = models.DateField()
    final_date         = models.DateField()
    faculty_mentor_date    = models.DateField()
    submit_whitepaper_date = models.DateField()

    event_info = models.TextField(blank=True, null=True)
    judging_criteria = models.TextField(blank=True, null=True)
    eligibility = models.TextField(blank=True, null=True)
    analysis_rubric = models.FileField(
        upload_to="analysis_rubric", blank=True, null=True
    )

    paper_guidelines = models.TextField(blank=True, null=True)
    entries_header   = models.TextField(blank=True, null=True)
    presentation     = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Check if the current event is being set as active
        if self.is_active:
            # Deactivate all other events
            Event.objects.exclude(pk=self.pk).update(is_active=False)

        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class EventPanel(TimestampedModel):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_panel"
    )
    speaker = models.ManyToManyField(User, related_name="panel_speaker")
    name    = models.CharField(max_length=50)
    title   = models.CharField(max_length=225)
    Description = models.TextField(null=True, blank=True)


class EventsSchedule(TimestampedModel):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_schedules"
    )
    panel = models.ForeignKey(
        EventPanel,
        on_delete=models.CASCADE,
        related_name="panel_schedule",
        null=True,
        blank=True,
    )
    speaker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="schedule_speaker",
        null=True,
        blank=True,
    )
    date     = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.event.title}"


class EventsTeam(TimestampedModel):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_teams"
    )
    team_creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="team_creator_user"
    )
    member = models.ManyToManyField(
        User, related_name="team_members", null=True, blank=True
    )
    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="team_mentor",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=225)
    image = models.ImageField(upload_to="Event/TeamImage", null=True, blank=True)
    topic_name = models.CharField(max_length=225, null=True, blank=True)
    invite_user = models.TextField(null=True, blank=True)
    white_paper = ArrayField(
        models.FileField(upload_to="Event/TeamWhitePaper", null=True, blank=True),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.event.title}, {self.name}"
