from django import forms
from django.forms import (
    ModelForm, TextInput, Select, CheckboxInput, NumberInput, FileInput, SelectMultiple, Textarea,
    PasswordInput, EmailInput, DateInput
)
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()

from apps.events.models import Event, EventPanel, EventsSchedule, EventsTeam


# class HelpfulResourcesForm(forms.ModelForm):
#     class Meta:
#         model = HelpfulResources
#         fields = '__all__'

#         widgets = {
#             'city'    : Select(attrs={   'class': 'form-select js-choice', 'id': 'city'}),
#             'location': TextInput(attrs={'class': 'form-control', 'id': 'location',  'placeholder': 'Enter home address'}),
#         }
    
        


class EventForm(forms.ModelForm):
    # property_image_form   = PropertyImageForm()
    # property_address_form = PropertyAddressForm()

    # property_image_form = PropertyImageForm(prefix='property_image')
    # property_address_form = PropertyAddressForm(prefix='property_address')

    class Meta:
        model = Event
        fields = [
            'title', 'banner_image', 'screen_image', 
            
            'register_team_date', 
            'select_topic_date', 
            'final_date', 
            'faculty_mentor_date', 
            'submit_whitepaper_date', 

            'event_info',
            'judging_criteria',
            'eligibility',
            'analysis_rubric',

            'paper_guidelines',
            'entries_header',
            'presentation',

            ]

        widgets = {
            'title' : Textarea(attrs={   
                'class': 'form-control', 
                'id'   : 'title',
                'rows' : '4',  
                'placeholder': 'Event Research Title'
            }),

            # Image Input
            'banner_image' : FileInput( attrs={
                'class': 'form-control', 
                'accept' : 'image/jpeg image/png image/jpg',
                'id': 'banner_image',
                # 'style': 'border-style: dotted;',
            }),
            'screen_image' : FileInput( attrs={
                'class': 'form-control', 
                'accept' : 'image/jpeg image/png image/jpg',
                'id': 'screen_image',
                # 'style': 'border-style: dotted;',
            }),
            'analysis_rubric' : FileInput( attrs={
                'class': 'form-control', 
                'id': 'analysis_rubric',
                # 'style': 'border-style: dotted;',
            }),
            

            # Date Input
            'register_team_date' : DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
            }),
            'select_topic_date' : DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
            }),
            'final_date' : DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
            }),
            'faculty_mentor_date' : DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
            }),
            'submit_whitepaper_date' : DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
            }),

            # Text Area
            'event_info' : Textarea(attrs={   
                'class': 'form-control', 
                'id'   : 'event_info',  
                'placeholder': 'Event Info.'
            }),
            'judging_criteria' : Textarea(attrs={   
                'class': 'form-control', 
                'id'   : 'judging_criteria',  
                'placeholder': 'Judging Criteria.'
            }),
            'eligibility' : Textarea(attrs={   
                'class': 'form-control', 
                'id'   : 'eligibility',  
                'placeholder': 'Eligibility.'
            }),
            'paper_guidelines' : Textarea(attrs={   
                'class': 'form-control', 
                'id'   : 'paper_guidelines',  
                'placeholder': 'Paper Guidelines.'
            }),
            'entries_header' : Textarea(attrs={   
                'class': 'form-control', 
                'id'   : 'entries_header',  
                'placeholder': 'Entries Header.'
            }),
            'presentation' : Textarea(attrs={   
                'class': 'form-control', 
                'id'   : 'presentation',  
                'placeholder': 'Presentation.'
            }),
            

        }