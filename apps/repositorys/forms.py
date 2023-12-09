from django import forms
from django.forms import (
    ModelForm, TextInput, Select, CheckboxInput, NumberInput, FileInput, SelectMultiple, Textarea,
    PasswordInput, EmailInput
)
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()

from apps.repositorys.models import (
    ResearchRepository, 
    HelpfulResources,
    TaprootCauses,
    ResponseStrategies, 
) 



# class HelpfulResourcesForm(forms.ModelForm):
#     class Meta:
#         model = HelpfulResources
#         fields = '__all__'

#         widgets = {
#             'city'    : Select(attrs={   'class': 'form-select js-choice', 'id': 'city'}),
#             'location': TextInput(attrs={'class': 'form-control', 'id': 'location',  'placeholder': 'Enter home address'}),
#         }
    
        


class ResearchRepositoryForm(forms.ModelForm):
    # property_image_form   = PropertyImageForm()
    # property_address_form = PropertyAddressForm()

    # property_image_form = PropertyImageForm(prefix='property_image')
    # property_address_form = PropertyAddressForm(prefix='property_address')

    class Meta:
        model = ResearchRepository
        fields = [
            'event', 'title', 'description', 
            # 'video', 'bed', 'bath',
            ]

        widgets = {
            'event' : Select(attrs={
                'class': 'form-select js-choice', 
                'id'   : 'event'
                }),

            'title' : TextInput(attrs={   
                'class': 'form-control', 
                'id'   : 'title',  
                'placeholder': 'Event Research Title'
                }),
            
            'description' : Textarea(attrs={   
                'class': 'form-control', 
                'id'   : 'title',  
                'placeholder': 'Event Research Description.'
                }),

        }