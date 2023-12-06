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



class EventCreateView(CreateView, LoginRequiredMixin):
    model = Event
    form_class = EventForm
    template_name = 'events/create_events.html'
    success_url = reverse_lazy('dashboards:home')
