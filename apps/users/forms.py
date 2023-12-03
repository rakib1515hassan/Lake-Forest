from django import forms
from django.forms import (
    ModelForm, TextInput, Select, CheckboxInput, NumberInput, FileInput, SelectMultiple, Textarea,
    PasswordInput, EmailInput
)

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()



class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Enter Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'profile_img', 'gender', 'dob',
                  'role', 'is_verified', 'is_admin', 'is_active',
                ]

        widgets = {
            'email' : EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Enter email'}),
            'name'  : TextInput( attrs={'class': 'form-control', 'id': 'name',  'placeholder': 'Enter name'}),
            'phone' : TextInput( attrs={'class': 'form-control', 'id': 'phone', 'placeholder': 'Enter phone number'}),

            'dob': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),

            'profile_img'    : FileInput( attrs={
                'class': 'form-control show-img', 
                'accept' : 'image/jpeg image/png image/jpg',
                'id': 'user_img',
                # 'style': 'border-style: dotted;',
                }),

            'is_verified' : CheckboxInput(attrs={'class': 'form-check-input', 'id': "is_verified", }),
            'is_active'   : CheckboxInput(attrs={'class': 'form-check-input', '  id': "is_active", }),
        }

    # IS_VERIFY_CHOICES = (
    #     (True, 'Yes'),
    #     (False, 'No'),
    # )

    # # Add ChoiceField for is_verify and specify RadioSelect widget
    # is_verified = forms.ChoiceField(
    #     choices=IS_VERIFY_CHOICES,
    #     widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    # )

    # IS_ACTIVE_CHOICES = (
    #     (True, 'Yes'),
    #     (False, 'No'),
    # )

    # # Add ChoiceField for is_active and specify RadioSelect widget
    # is_admin = forms.ChoiceField(
    #     choices=IS_ACTIVE_CHOICES,
    #     widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    # )

    USER_ROLE_CHOICES = (
        ('member', 'member'),
        ('mentor', 'mentor'),
    )

    role = forms.ChoiceField(
        choices = USER_ROLE_CHOICES,
        widget  = Select(attrs={'class': 'form-select js-choice', 'id': 'role'})
    )


    gender = forms.ChoiceField(
        choices = User.GenderType.choices,
        # initial = 'male',  # Set the initial/default value here
        widget  = Select(attrs={'class': 'form-select js-choice', 'id': 'gender'})
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match!")
        if password1 and len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        return password2
    

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)

        # print("--------------------")
        # print("User = ", self.cleaned_data["name"])
        # print("--------------------")

        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    


## For Django Admin Panel
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        # fields = ['name', 'email', 'phone', 'user_img', 'user_type', 'is_verified']
        fields = ['name', 'email', 'phone', 'profile_img', 'role', 'is_verified', 'is_admin']

    def clean_password(self):
        return self.initial['password']
    




class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'profile_img']

        widgets = {
            'email' : EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Enter email'}),
            'name'  : TextInput( attrs={'class': 'form-control', 'id': 'name',  'placeholder': 'Enter name'}),
            'phone' : TextInput( attrs={'class': 'form-control', 'id': 'phone', 'placeholder': 'Enter phone number'}),

            'user_img'    : FileInput( attrs={'class': 'form-control', 'id': 'user_img'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        user_img = cleaned_data.get('user_img')
        user_cov_img = cleaned_data.get('user_cov_img')

        if not user_img:
            instance = self.instance
            cleaned_data['user_img'] = instance.user_img
            
        if not user_cov_img:
            instance = self.instance
            cleaned_data['user_cov_img'] = instance.user_cov_img

        return cleaned_data
    
