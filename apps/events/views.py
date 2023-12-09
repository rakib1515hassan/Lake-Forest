from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme

from django.views import View
# from django.views.generic.edit import UpdateView
from django.views.generic import (
        ListView, 
        DetailView, 
        CreateView,
        UpdateView, 
        DeleteView, 
        TemplateView, 
        RedirectView,
    )
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from apps.dashboards.permission import is_superuser_or_staff
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.urls import reverse_lazy, reverse
from apps.events.models import Event, EventPanel, EventsSchedule, EventsTeam
from apps.events.forms import EventForm

@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url='/admin/users/login/?next'), name='dispatch')
class EventListView(ListView, LoginRequiredMixin):
    model = Event
    template_name = 'events/list_events.html'
    context_object_name = 'events'
    obj_per_page = 10

    def get_queryset(self):
        queryset = Event.objects.all().order_by('-created_at')
        search_query = self.request.GET.get('search', '')  

        if search_query:
            queryset = queryset.filter(
                    Q(title__icontains  = search_query) | 
                    Q(paper_guidelines__icontains = search_query) |
                    Q(entries_header__icontains = search_query) |
                    Q(presentation__icontains = search_query)
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users   = self.get_queryset()
        paginator   = Paginator(users, self.obj_per_page)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            raise Http404("Page not found")
        context['products'] = page_obj
        context['page_obj'] = page_obj
        context['products_count'] = users.count()
        return context



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url='/admin/users/login/?next'), name='dispatch')
class EventDetailView(DetailView, LoginRequiredMixin):
    model = Event
    template_name = 'events/details.html'
    context_object_name = 'event'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["location"] = location
    #     return context


@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url='/admin/users/login/?next'), name='dispatch')
class EventCreateView(CreateView, LoginRequiredMixin):
    model = Event
    form_class = EventForm
    template_name = 'events/create_events.html'
    success_url = reverse_lazy('dashboards:home')




"""
        Event Panel
"""

@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url='/admin/users/login/?next'), name='dispatch')
class EventPanelsCreateView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        event_id = request.POST.get('event') 
        speaker_ids = request.POST.getlist('speaker')
        name = request.POST.get('name')
        title = request.POST.get('title')
        description = request.POST.get('description')

        print("------------------")
        print("event_id = ", event_id)
        print("speaker_ids = ", speaker_ids)
        print("name = ", name)
        print("title = ", title)
        print("description = ", description)
        print("------------------")

        # Create EventPanel instance and save
        if event_id and speaker_ids:
            event_panel = EventPanel.objects.create(
                    event_id=event_id,
                    name=name,
                    title=title,
                    description=description
                )
            event_panel.speaker.set(speaker_ids)

        return redirect('events:events-panel-list')


@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url='/admin/users/login/?next'), name='dispatch')
class EventPanelsListView(ListView, LoginRequiredMixin):
    model = EventPanel
    template_name = 'events/Others/list_panel.html'
    context_object_name = 'panels'
    obj_per_page = 10

    def get_queryset(self):
        event = Event.objects.filter(is_active = True).first()
        queryset = EventPanel.objects.filter(event = event)

        # search_query = self.request.GET.get('search', '')  

        # if search_query:
        #     queryset = queryset.filter(
        #             Q(title__icontains  = search_query) | 
        #             Q(paper_guidelines__icontains = search_query) |
        #             Q(entries_header__icontains = search_query) |
        #             Q(presentation__icontains = search_query)
        #         )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        panels   = self.get_queryset()
        paginator   = Paginator(panels, self.obj_per_page)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            raise Http404("Page not found")
    
        context['event'] = Event.objects.filter(is_active = True).first()
        context['speakers'] = User.objects.filter(role = 'mentor')
        context['page_obj'] = page_obj
        context['products_count'] = panels.count()
        return context
    




"""
        Events Schedule
"""

@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url='/admin/users/login/?next'), name='dispatch')
class EventsScheduleCreateView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        event_id = request.POST.get('event') 

        panel_id = request.POST.get('panel')
        speaker_id = request.POST.get('speaker')

        date     = request.POST.get('date')
        s_time   = request.POST.get('s_time')
        e_time   = request.POST.get('e_time')
        location = request.POST.get('location')

        print("------------------")
        print("event_id = ", event_id)
        print("panel_ids = ", panel_id)
        print("speaker_ids = ", speaker_id)

        print("date = ", date)
        print("s_time = ", s_time)
        print("e_time = ", e_time)
        print("location = ", location)
        print("------------------")

        # Create EventPanel instance and save
        if event_id:
            event_schedule = EventsSchedule.objects.create(
                    event_id=event_id,
                    date   = date,
                    start_time = s_time,
                    end_time = e_time,
                    location = location,
                )
            # Get the actual EventPanel and User instances
            panel_instance = get_object_or_404(EventPanel, id=panel_id)
            speaker_instance = get_object_or_404(User, id=speaker_id)

            # Assign the instances to the ForeignKey fields
            event_schedule.panel = panel_instance
            event_schedule.speaker = speaker_instance

            event_schedule.save()
        return redirect('events:events-schedule-list')
    



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url='/admin/users/login/?next'), name='dispatch')
class EventsScheduleListView(ListView, LoginRequiredMixin):
    model = EventsSchedule
    template_name = 'events/Others/list_schedule.html'
    context_object_name = 'schedules'
    obj_per_page = 10

    def get_queryset(self):
        event = Event.objects.filter(is_active = True).first()
        queryset = EventsSchedule.objects.filter(event = event)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule   = self.get_queryset()
        paginator   = Paginator(schedule, self.obj_per_page)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            raise Http404("Page not found")
    
        context['event'] = Event.objects.filter(is_active = True).first()
        context['panels'] = EventPanel.objects.filter(event = context['event'])
        context['speakers'] = User.objects.filter(role = 'mentor')
        context['page_obj'] = page_obj
        context['products_count'] = schedule.count()
        return context