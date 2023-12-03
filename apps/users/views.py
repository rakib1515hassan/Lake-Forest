# from django.shortcuts import render, redirect
# from django.contrib.auth import get_user_model
# User = get_user_model()

# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
# from django.db.models import Q
# from django.http import HttpRequest, HttpResponse, JsonResponse
# from django.utils.http import url_has_allowed_host_and_scheme

# from django.views import View
# from django.views.generic.edit import UpdateView
# from django.views.generic import (
#     ListView, 
#     DetailView, 
#     CreateView,
#     # UpdateView, 
#     DeleteView, 
#     TemplateView, 
#     RedirectView,
# )
# from apps.users.forms import UserCreationForm, UserUpdateForm
# from django.urls import reverse
# from django.contrib.auth.decorators import user_passes_test
# from django.utils.decorators import method_decorator
# from apps.dashboards.permission import is_superuser_or_staff
# from django.shortcuts import get_object_or_404
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import Http404


# """
#     Admin Login
#     @Rakib
# """
# class LoginView(View):
#     template_name = "users/login.html"

#     def get(self, request, *args, **kwargs):
#         # Check if the user is already authenticated, and if so, redirect them to their requested page.
#         if request.user.is_authenticated:
#             next_url = request.GET.get('next')
#             if next_url and url_has_allowed_host_and_scheme(next_url, request.get_host()):
#                 return redirect(next_url)
#             return redirect('dashboards:home')  # Redirect to the home page by default if no valid 'next' parameter.
        
#         return render(request, self.template_name)


#     def post(self, request, *args, **kwargs):
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         if User.objects.filter(email=email).first():
#             auth_user = authenticate(request, email=email, password=password)

#             if auth_user is not None:
#                 if auth_user.is_admin == True:
#                     login(request, auth_user)
#                     next_url = request.GET.get('next')

#                     if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
#                         return redirect(next_url)
#                     return redirect('dashboards:home')
                
#                 else:
#                     error = 'Only admin users can login.'
#                     return render(request, self.template_name, {'error': error})

#             else:
#                 response = {
#                     'error': 'Invalid password',
#                     'error_type': 'Password',
#                     }
#                 return render(request, self.template_name, response)

#         else:
#             response = {
#                 'error': 'Invalid email.', 
#                 'error_type':'Email'}
#             return render(request, self.template_name, response)


    


# """
#     Admin Logout
#     @Rakib
# """
# @method_decorator(user_passes_test(is_superuser_or_staff, 
#     login_url='/admin/users/login/?next'), name='dispatch')
# class LogoutView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             logout(request)
#         return render(request, "users/logout.html")
    


# """
#     Other's user can login
#     @Rakib
# """
# class RestrictedView(View, LoginRequiredMixin):
#     def get(self, request):
#         if request.user.is_authenticated:
#             return render(request, "users/restricted.html")
#         else:
#            return redirect('users:login')
        


# """
#     All User get in admin panel
#     @Rakib
# """
# @method_decorator(user_passes_test(is_superuser_or_staff, 
#     login_url='/admin/users/login/?next'), name='dispatch')
# class UserListView(ListView, LoginRequiredMixin):
#     model = User
#     template_name = "users/user/list.html"
#     context_object_name = "users"
#     obj_per_page = 10
    
#     def get_queryset(self):
#         queryset = User.objects.all().order_by('-created_at').exclude(is_admin = True)
#         search_query = self.request.GET.get('search', '')  

#         if search_query:
#             queryset = queryset.filter(
#                     Q(name__icontains  = search_query) | 
#                     Q(email__icontains = search_query) |
#                     Q(phone__icontains = search_query) |
#                     Q(user_type__icontains = search_query)
#                 )

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         users = self.get_queryset()

#         paginator = Paginator(users, self.obj_per_page)
#         page_number = self.request.GET.get('page')

#         try:
#             page_obj = paginator.get_page(page_number)
#         except EmptyPage:
#             raise Http404("Page not found")

#         context['products'] = page_obj
#         context['page_obj'] = page_obj
#         context['products_count'] = users.count()
#         return context
    


# """
#     User create by admin
#     @Rakib
# """
# @method_decorator(user_passes_test(is_superuser_or_staff, 
#     login_url='/admin/users/login/?next'), name='dispatch')
# # class UserCreateView(CreateView, LoginRequiredMixin):
# #     model = User
# #     form_class    = UserCreationForm
# #     template_name = "users/user/create.html"
# #     success_url   = "/admin/users/user-list/"

# #     def post(self, request, *args, **kwargs):
# #         form = self.get_form()
# #         if form.is_valid():
# #             form.save()
# #             return redirect(self.success_url)
# #         else:
# #             return self.form_invalid(form)
            
# #     def form_invalid(self, form):
# #         return render(self.request, self.template_name, {'form': form})

# class UserCreateView(CreateView, LoginRequiredMixin):
#     model = User
#     form_class = UserCreationForm
#     template_name = "users/user/create.html"
#     success_url = "/admin/users/user-list/"

#     # def form_valid(self, form):
#     #     form.save()
#     #     return super().form_valid(form)

#     def form_invalid(self, form):
#         field_errors = {field.name: field.errors for field in form}
#         has_errors = any(field_errors.values())

#         return self.render_to_response(self.get_context_data(
#             form=form, 
#             field_errors=field_errors, 
#             has_errors=has_errors
#             ))

    

#     # return self.form_invalid(form)
#     # return self.render_to_response(self.get_context_data(form=form))




# """
#     User details for admin
#     @Rakib
# """
# @method_decorator(user_passes_test(is_superuser_or_staff, 
#     login_url='/admin/users/login/?next'), name='dispatch')
# class UserDetailsView(DetailView, LoginRequiredMixin):
#     model = User
#     template_name = "users/user/detail.html"
#     context_object_name = "user"

#     def get_context_data(self, *args, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['user'] = self.model.objects.get(id=self.kwargs['pk'])
#         # Print a message to the console
#         # user = data['user']  # Access the user from the data dictionary
#         # print("----------------------------")
#         # print(f"User details displayed: {user.email} ({user.id})")
#         # print("----------------------------")
#         return data

    

#     # class UserDetailView(DetailView):
#     #     model = User
#     #     template_name = "users/user/detail.html"
#     #     context_object_name = "user"

#     #     def get_object(self, queryset=None):
#     #         user = User.objects.get(id=self.kwargs['pk'])
            
#     #         # Print a message to the console
#     #         print(f"User details displayed: {user.username} ({user.id})")

#     #         return user




# """
#     User update by admin
#     @Rakib
# """
# @method_decorator(user_passes_test(is_superuser_or_staff, 
#     login_url='/admin/users/login/?next'), name='dispatch')
# class UserUpdateView(UpdateView, LoginRequiredMixin):
#     model = User
#     template_name = "users/user/update.html"
#     form_class = UserUpdateForm
#     context_object_name = "user"

#     def get_success_url(self):
#         return reverse('users:user-details', kwargs={'pk': self.object.pk})
    
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         field_errors = {field.name: field.errors for field in form}
#         has_errors = any(field_errors.values())

#         # print("---------------------")
#         # print(f"Field = {field_errors}, HasErrors = {has_errors}")
#         # print(f"HasErrors = {has_errors}")
#         # print("---------------------")

#         return self.render_to_response(self.get_context_data(
#             form=form, 
#             field_errors=field_errors, 
#             has_errors=has_errors
#             ))
    



# """
#     User password change by admin
#     @Rakib
# """
# @method_decorator(user_passes_test(is_superuser_or_staff, 
#     login_url='/admin/users/login/?next'), name='dispatch')
# class UserChangePasswordView(View, LoginRequiredMixin):
#     def post(self, request, *args, **kwargs):
#         new_password = request.POST.get('n_password')
#         con_password = request.POST.get('c_password')
#         user_id      = self.kwargs.get('user_id', None)

#         if new_password != con_password :
#             return JsonResponse({'success': False, 'error': "Passwords didn't match! Try again."})
        
#         if len(str(new_password)) < 8:
#             return JsonResponse({'success': False, 'error': "Password length must be at least 8. Try again."})
        
#         try:
#             user = User.objects.get(id = user_id)

#             if user and new_password:
#                 user.set_password(new_password)
#                 user.save()
#                 return JsonResponse({'success': True})
#             else:
#                 return JsonResponse({'success': False, 'error': 'New password is required'})
#         except User.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'User does not exist!'})





# """
#     User permission update by admin
#     @Rakib
# """
# @method_decorator(user_passes_test(is_superuser_or_staff, 
#     login_url='/admin/users/login/?next'), name='dispatch')
# class UserPermissionUpdateView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             user = User.objects.get(id = kwargs['user_id'])
#             data = request.POST

#             superadmin = str(data.get('is_superadmin'))
#             admin      = str(data.get('is_admin'))
#             user_type  = data.get('user_type')
#             active     = data.get('is_active')
#             verify     = data.get('is_verified')

#             if user:

#                 if superadmin == str(1) and admin == str(1):
#                     user.is_superuser = True
#                     user.is_admin     = True
#                     user.user_type    = 'admin'

#                 elif superadmin == str(0) and admin == str(1):
#                     user.is_superuser = False
#                     user.is_admin     = True
#                     user.user_type    = 'admin'

#                 elif superadmin == str(0) and  admin == str(0):
#                     user.is_admin = False
#                     user.user_type = 'customer'

#                 if user_type:
#                     if user_type != user.user_type:
#                         user.user_type = user_type

#                 if (active and verify):
#                     if active != user.is_active:
#                         user.is_active = active
#                     if verify != user.is_verified:
#                         user.is_verified = verify

#                 user.save()
#                 response_data = {'success': True}
#                 return JsonResponse(response_data)
        
#         except User.DoesNotExist:
#             response_data = {'success': False}
#             return JsonResponse(response_data)
    


# @method_decorator(user_passes_test(is_superuser_or_staff, 
#     login_url='/admin/users/login/?next'), name='dispatch')
# class UserDeleteView(DeleteView):
#     model = User
#     success_url = '/admin/users/user-list/'

#     def post(self, request, user_id):
#         try:
#             user = User.objects.get(id = user_id)
#             if user:
#                 user.delete()
#                 # messages.success(request, 'User deleted successfully!')
#                 return redirect(self.success_url)
#         except User.DoesNotExist:
#             # messages.error(request, "Error is occurred. Please try again!")
#             return redirect(self.success_url)
