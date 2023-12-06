from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme

from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    # UpdateView, 
    DeleteView, 
    TemplateView, 
    RedirectView,
)
from apps.users.forms import UserCreationForm, UserUpdateForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from apps.dashboards.permission import is_superuser_or_staff
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.urls import reverse_lazy, reverse

# Create your views here.
# @method_decorator(user_passes_test(is_superuser_or_staff, 
#     login_url=reverse_lazy('dashboards:login')), name='dispatch')
# def Home(request):
#     # return HttpResponse("Hellow Lake Forest....")
#     return render(request, 'home.html')



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class Home(LoginRequiredMixin, TemplateView):
    login_url = "/admin/users/login/"
    redirect_field_name = "login"
    template_name = "home.html"
    # template_name = "dashboards/dashboard.html"

    # def get(self, request, *args, **kwargs):

    #     users = User.objects.all().exclude(is_superuser=True)
    #     total_user = users.count()
    #     # Get all active sessions
    #     active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    #     # Count the unique users with active sessions
    #     logged_in_users = len(set(s.get_decoded().get('_auth_user_id') for s in active_sessions))


    #     customers  = users.filter(user_type='customer').count()
    #     sellers    = users.filter(user_type='seller').count()

    #     property = Property.objects.all()
    #     total_property   = property.all().count()
    #     property_pending = property.filter(property_status = 'pending').count()

        



    #     ## Map
    #     m = folium.Map(
    #         location   = [23.8103, 90.4125], 
    #         zoom_start = 8,
    #         # position="absolute",
    #         # left="0%",
    #         # width="100%",
    #         # height="100%",
    #     )

    #     pro_addresses = PropertyAddress.objects.all()
    #     latitudes  = [address.latitude  for address in pro_addresses]
    #     longitudes = [address.longitude for address in pro_addresses]
    #     FastMarkerCluster(data = list(zip(latitudes, longitudes))).add_to(m)

        
    #     # Find the top cityes
    #     top_cities = PropertyAddress.objects.values('city').annotate(city_count=Count('city')).order_by('-city_count')[:3]

    #     for city in top_cities:
    #         print("---------------------")
    #         print(f"City: {city['city']}, Count: {city['city_count']}")
    #         print("---------------------")

    #     data = {
    #         'map': m._repr_html_(),
    #         'total_users': total_user,
    #         'logged_in_users' : logged_in_users,
    #         'customers'  : customers,
    #         'sellers'    : sellers,
    #         'total_property' : total_property,
    #         'property_pending' : property_pending,
    #         'top_cities' : top_cities,
    #     }

    #     return render(request, self.template_name, data)
    

# def LiveDashboard_Data(request):

#     users = User.objects.all().exclude(is_superuser=True)
#     total_user = users.count()
#     # Get all active sessions
#     active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
#     # Count the unique users with active sessions
#     logged_in_users = len(set(s.get_decoded().get('_auth_user_id') for s in active_sessions))

#     customers  = users.filter(user_type='customer').count()
#     sellers    = users.filter(user_type='seller').count()

#     property = Property.objects.all()
#     total_property   = property.all().count()
#     property_pending = property.filter(property_status = 'pending').count()
    
#     data = {
#         'total_user': total_user,
#         'logged_in_users': logged_in_users,
#         'customers'  : customers,
#         'sellers'    : sellers,
#         'total_property' : total_property,
#         'property_pending' : property_pending,
#     }
#     return JsonResponse(data)




"""
    Admin Login
"""
class LoginView(View):
    template_name = "dashboards/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, request.get_host()):
                return redirect(next_url)
            return redirect('dashboards:home')
        
        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).first():
            auth_user = authenticate(request, email=email, password=password)

            if auth_user is not None:
                if (auth_user.is_admin == True) or (auth_user.is_superuser == True):
                    print("------------------------")
                    print("email = ", email)
                    print("password = ", password)
                    print("auth_user = ", auth_user)
                    print("------------------------")
                    login(request, auth_user)
                    next_url = request.GET.get('next')

                    if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                        return redirect(next_url)
                    return redirect('dashboards:home')
                
                else:
                    error = 'Only admin users can login.'
                    return render(request, self.template_name, {'error': error})

            else:
                response = {
                    'error': 'Invalid password',
                    'error_type': 'Password',
                    }
                return render(request, self.template_name, response)

        else:
            response = {
                'error': 'Invalid email.', 
                'error_type':'Email'}
            return render(request, self.template_name, response)


    


"""
    Admin Logout
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('dashboards:login')), name='dispatch')
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, "dashboards/logout.html")
    


"""
    Other's user can login
"""
class RestrictedView(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "dashboards/restricted.html")
        else:
           return redirect('dashboards:login')