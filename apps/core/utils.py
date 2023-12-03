from datetime import datetime

import requests
from django.db.models import Q
from django.db.models.fields.files import ImageFieldFile
from django.http import JsonResponse
from django.urls import reverse
from django.utils.html import strip_tags
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from lake_forest import settings
from django.core.mail import EmailMultiAlternatives

def api_success(results, status=200, message="Operation successful"):
    if results is None:
        results = {}
    data = {'success': True, "message": message}
    if "results" in results:
        data.update(results)
    else:
        data["results"] = results

    return Response(data, status=status)


def api_error(data, status=400, message="Something went wrong!"):
    if data is None:
        data = {}

    if not isinstance(data, dict):
        data = {'results': data}
    data['success'] = False
    data["message"] = message
    return Response(data, status=status)



def create_JWT_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class ApiBaseView(APIView, LimitOffsetPagination):
    default_limit = settings.DEFAULT_PAGINATION_LIMIT
    max_limit = 100

    def __init__(self, **kwargs):
        # check if child class has Meta class
        super().__init__(**kwargs)
        if hasattr(self, 'Meta'):

            # check if Meta class has model and serializer
            if hasattr(self.Meta, 'model') and hasattr(self.Meta, 'serializer'):
                self.model = self.Meta.model
                self.serializer = self.Meta.serializer
                self.paginate_by = self.Meta.paginate_by if hasattr(self.Meta, 'paginate_by') else 10
                self.only_methods = self.Meta.only_methods if hasattr(self.Meta, 'only_methods') else None
                self.exclude_methods = self.Meta.exclude_methods if hasattr(self.Meta, 'exclude_methods') else None
            else:
                raise Exception('Meta class must have model and serializer!')
        else:
            raise Exception('Meta class is required!')

    def _access_decorator(func):
        def wrapper(*args, **kwargs):
            if args[0].only_methods:
                if func.__name__ not in args[0].only_methods:
                    return Response({'details': 'Method not allowed!'}, status=405)
            if args[0].exclude_methods:
                if func.__name__ in args[0].exclude_methods:
                    return Response(status=403)
            return func(*args, **kwargs)

        return wrapper

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound({
                'success': False,
                'message': 'Object does not exist!',
                'errors': {}
            }, 404)

    @_access_decorator
    def get(self, request, pk=None, format=None):
        if pk:
            obj = self.get_object(pk)
            serializer = self.serializer(obj)
            return api_success(serializer.data)

        # get all keys from model
        model_keys = [field.name for field in self.model._meta.get_fields()]

        # get all keys from request query params
        query_keys = [key for key in request.query_params.keys()]

        sort_by = request.query_params.get('sort_by', None)
        order = request.query_params.get('order', None)

        # if request has sort_by and order params, separate them
        if 'sort_by' in query_keys:
            query_keys.remove('sort_by')
        if 'order' in query_keys:
            query_keys.remove('order')

        filter_q = {}

        # if request has query params, filter model
        if query_keys:
            for key in query_keys:
                k = key.split('_')
                if k[0] in model_keys:
                    if len(k) == 1:
                        filter_q[k[0]] = request.query_params.get(key)
                    elif len(k) == 2:
                        if k[1] == 'contains':
                            filter_q[f'{k[0]}__contains'] = request.query_params.get(key)
                        elif k[1] == 'icontains':
                            filter_q[f'{k[0]}__icontains'] = request.query_params.get(key)
                        elif k[1] == 'startswith':
                            filter_q[f'{k[0]}__startswith'] = request.query_params.get(key)
                        elif k[1] == 'istartswith':
                            filter_q[f'{k[0]}__istartswith'] = request.query_params.get(key)
                        else:
                            return api_error(
                                {'errors': {key: 'Invalid query param'}},
                                status=422,
                                message="Validation error!"
                            )

        if filter_q:
            data = self.model.objects.filter(**filter_q)
        else:
            data = self.model.objects.all()

        if sort_by:
            if sort_by in model_keys:
                if order == 'desc':
                    data = data.order_by(f'-{sort_by}')
                else:
                    data = data.order_by(sort_by)
            else:
                return api_error(
                    {'errors': {'sort_by': 'Invalid sort by field!'}},
                    status=422,
                    message="Validation error!"
                )

        page = self.paginate_queryset(data, request, view=self)
        serializer = self.serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @_access_decorator
    def post(self, request, format=None):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            try:
                if hasattr(serializer.Meta, 'extra_kwargs'):
                    extra_kwargs = serializer.Meta.extra_kwargs
                    for key in extra_kwargs:
                        serializer.validated_data[key] = request.data.get(key, None)

                serializer.save()
                return api_success(serializer.data, status=201)

            except Exception as e:
                return api_error({'errors': {'error': str(e)}}, status=422, message="Validation error!")

        return api_error({'errors': serializer.errors}, status=422, message="Validation error!")

    @_access_decorator
    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.serializer(obj, data=request.data)
        if serializer.is_valid():
            if hasattr(serializer.Meta, 'extra_kwargs'):
                extra_kwargs = serializer.Meta.extra_kwargs
                for key in extra_kwargs:
                    serializer.validated_data[key] = request.data.get(key, None)

            serializer.save()
            return api_success(serializer.data)
        return api_error({'errors': serializer.errors}, status=422, message="Validation error!")

    @_access_decorator
    def delete(self, request, pk=None, format=None):
        if pk:
            obj = self.get_object(pk)
            obj.delete()
            return api_success({
                "success": True,
            }, status=200)
        else:
            ids = request.data.get('ids', [])
            if ids:
                self.model.objects.filter(id__in=ids).delete()
                return api_success({
                    "success": True,
                }, status=200)


def method_decorator(method):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if args[0].request.method not in method:
                return Response(status=405)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validation_errors(errors):
    return api_error({'errors': errors}, status=422, message="Validation error!")


class BaseSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.Meta, 'extra_kwargs'):
            extra_kwargs = self.Meta.extra_kwargs
            for key in extra_kwargs:
                self.fields[key] = extra_kwargs[key]

    def validate(self, data):
        if hasattr(self.Meta, 'extra_kwargs'):
            extra_kwargs = self.Meta.extra_kwargs
            for key in extra_kwargs:
                data[key] = self.initial_data.get(key, None)
        return data

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(self.Meta, 'extra_kwargs'):
            extra_kwargs = self.Meta.extra_kwargs
            for key in extra_kwargs:
                data[key] = getattr(instance, key)
        return data

    def to_internal_value(self, data):
        if hasattr(self.Meta, 'extra_kwargs'):
            extra_kwargs = self.Meta.extra_kwargs
            for key in extra_kwargs:
                data[key] = self.initial_data.get(key, None)
        return super().to_internal_value(data)

    class Meta:
        model = None
        serializer = None
        extra_kwargs = None


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


def get_datatable(request, param, model, config):
    if param == 'config':
        return JsonResponse(config)

    elif param == 'action':
        if request.method == 'POST':
            type = request.POST.get('type')
            id = request.POST.get('id')
            if type == 'delete':
                model.get(pk=id).delete()
                return JsonResponse({
                    'status': 'success',
                    'type': 'silent',
                })
            else:
                route_name = request.POST.get('route')
                return JsonResponse({
                    'status': 'success',
                    'type': 'redirect',
                    'url': reverse(route_name, args=(id,))
                })

    elif param == 'data':
        sort_by = request.GET.get('sort_by', config['columns'][0]['source'])
        order_by = request.GET.get('order_by', 'asc')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))

        if search:
            search_columns = [column['source'] for column in config['columns'] if column.get('searchable')]
            or_lookup = Q()
            if search_columns:
                for column in search_columns:
                    or_lookup = or_lookup | Q(**{f"{column}__icontains": search})
                data = model.filter(or_lookup)
            else:
                data = model.all()
        else:
            data = model.all()

        total = data.count()
        if sort_by:
            if order_by == 'asc':
                data = data.order_by(sort_by)
            else:
                data = data.order_by(f"-{sort_by}")

        data = data[(page - 1) * limit:page * limit]

        data_as = []
        sources = [column['source'] for column in config['columns']]
        for obj in data:
            row = {}
            for source in sources:
                d = getattr(obj, source, None)
                if not d:
                    row[source] = None

                elif isinstance(d, datetime):
                    row[source] = d.strftime('%d/%m/%Y')
                elif isinstance(d, ImageFieldFile):
                    row[source] = d.url
                else:
                    row[source] = d

            data_as.append(row)

        return JsonResponse({
            'data': data_as,
            'total': total,
        })


# def html_mail_sender(subject, html_content, to, from_email=None):
#     try:
#         from django.core.mail import EmailMultiAlternatives

#         if not from_email:
#             from_email = "AddressPMS <" + settings.EMAIL_HOST_USER + ">"

#         # from_email   = settings.EMAIL_HOST_USER
#         text_content = strip_tags(html_content)

#         # print("------------------")
#         # print("subject =    ", subject)
#         # print("Body =       ", html_content)
#         # print("from_email = ", from_email) 
#         # print("to_email =   ", [to])
#         # print("------------------")

#         email = EmailMultiAlternatives(subject, text_content, from_email, [to])
#         email.attach_alternative(html_content, "text/html")
#         return email.send()
#     except Exception as e:
#         print(e)
#         return None
    
def html_mail_sender(subject, html_content, to, from_email=None):
    try:
        from django.core.mail import EmailMultiAlternatives

        if not from_email:
            from_email = "LakeForest <" + settings.EMAIL_HOST_USER + ">"

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, "text/html")
        return email.send()
    except Exception as e:
        print(e)
        return None


def sms_sender(phone, msg):
    try:
        greenweburl = "http://api.greenweb.com.bd/api.php"
        token = "b32c40d07064593e7576f55802b46b1d"

        # sms receivers number here (separated by comma)
        to = "+880" + phone[-10:]

        if len(to) != 14:
            raise Exception('Invalid phone number!')

        data = {
            'token': token,
            'to': to,
            'message': 'Konnect\n' + msg,
        }

        responses = requests.post(url=greenweburl, data=data)
        return responses.text

    except Exception as e:
        print(e)
        return None
