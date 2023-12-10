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
from apps.events.forms import EventForm, EventPanelForm

@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
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
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventDetailView(DetailView, LoginRequiredMixin):
    model = Event
    template_name = 'events/details.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teams"] = EventsTeam.objects.filter(event = Event.objects.first())[:10]
        context["panels"] = EventPanel.objects.filter(event = Event.objects.first())[:10]
        return context


@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventCreateView(CreateView, LoginRequiredMixin):
    model = Event
    form_class = EventForm
    template_name = 'events/create_events.html'
    success_url = reverse_lazy('events:events-list')



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return JsonResponse({'message': 'Deleted successfully'})



class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/update.html'
    success_url = reverse_lazy('events:events-list')


        


"""
        Event Panel
"""

@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
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
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventPanelsListView(ListView, LoginRequiredMixin):
    model = EventPanel
    template_name = 'events/Others/Panel/list_panel.html'
    context_object_name = 'panels'
    obj_per_page = 10

    def get_queryset(self):
        event = Event.objects.first()
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
    
        context['event'] = Event.objects.first()
        context['speakers'] = User.objects.filter(role = 'mentor')
        context['page_obj'] = page_obj
        context['products_count'] = panels.count()
        return context
    


@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventPanelsDeleteView(DeleteView):
    model = EventPanel
    def post(self, request, pk):
        event = get_object_or_404(EventPanel, id=pk)
        event.delete()
        return JsonResponse({'message': 'Deleted successfully'})
    


@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventPanelsUpdateView(LoginRequiredMixin, UpdateView):
    model = EventPanel
    form_class = EventPanelForm
    template_name = 'events/Others/Panel/update.html'
    success_url = reverse_lazy('events:events-panel-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.first()
        return context

    def form_valid(self, form):
        event = Event.objects.first()
        form.instance.event = event
        form.save()
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     field_errors = {field.name: field.errors for field in form}
    #     has_errors = any(field_errors.values())

    #     print("------------------")
    #     print("Error =", field_errors)
    #     print("------------------")

    #     return self.render_to_response(self.get_context_data(
    #         form=form, 
    #         field_errors=field_errors, 
    #         has_errors=has_errors
    #         ))



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventPanelsDetailView(DetailView, LoginRequiredMixin):
    model = EventPanel
    template_name = 'events/Others/Panel/details.html'
    context_object_name = 'panel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.first()
        return context
    


"""
        Events Schedule
"""

@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
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
            if panel_id:
                panel_instance = get_object_or_404(EventPanel, id=panel_id)
                if panel_instance is not None:
                    event_schedule.panel = panel_instance
            
            if speaker_id:
                speaker_instance = get_object_or_404(User, id=speaker_id)
                if speaker_instance is not None:
                    event_schedule.speaker = speaker_instance

            
            

            event_schedule.save()
        return redirect('events:events-schedule-list')
    



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventsScheduleListView(ListView, LoginRequiredMixin):
    model = EventsSchedule
    template_name = 'events/Others/Schedule/list_schedule.html'
    context_object_name = 'schedules'
    obj_per_page = 10

    def get_queryset(self):
        event = Event.objects.first()
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
    
        context['event'] = Event.objects.first()
        context['panels'] = EventPanel.objects.filter(event = context['event'])
        context['speakers'] = User.objects.filter(role = 'mentor')
        context['page_obj'] = page_obj
        context['products_count'] = schedule.count()
        return context
    


@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventsScheduleDeleteView(DeleteView):
    model = EventsSchedule
    def post(self, request, pk):
        event = get_object_or_404(EventsSchedule, id=pk)
        print("------------------")
        print("event")
        print("------------------")
        event.delete()
        return JsonResponse({'message': 'Deleted successfully'})




@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventsScheduleDetailView(DetailView, LoginRequiredMixin):
    model = EventsSchedule
    template_name = 'events/Others/Schedule/details.html'
    context_object_name = 'schedule'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.first()
        return context
    




    """
        Events Team
"""

@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventsTeamCreateView(View, LoginRequiredMixin):
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
            events_team = EventsTeam.objects.create(
                    event_id=event_id,
                    date   = date,
                    start_time = s_time,
                    end_time = e_time,
                    location = location,
                )
            # Get the actual EventPanel and User instances
            panel_instance   = get_object_or_404(EventPanel, id=panel_id)
            speaker_instance = get_object_or_404(User, id=speaker_id)

            # Assign the instances to the ForeignKey fields
            events_team.panel = panel_instance
            events_team.speaker = speaker_instance

            events_team.save()
        return redirect('events:events-schedule-list')
    



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class EventsTeamListView(ListView, LoginRequiredMixin):
    model = EventsTeam
    template_name = 'events/Others/Team/list_team.html'
    context_object_name = 'teams'
    obj_per_page = 10

    def get_queryset(self):
        event = Event.objects.first()
        queryset = EventsTeam.objects.filter(event = event)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team   = self.get_queryset()
        paginator   = Paginator(team, self.obj_per_page)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            raise Http404("Page not found")
    
        context['event'] = Event.objects.first()
        context['members'] = User.objects.filter(role = 'member')
        context['mentors'] = User.objects.filter(role = 'mentor')
        context['page_obj'] = page_obj
        context['products_count'] = team.count()
        return context