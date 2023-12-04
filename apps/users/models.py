from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.users.manager import UserManager
import uuid
from apps.core.models import TimestampedModel, City
from rest_framework_simplejwt.tokens import RefreshToken

import secrets
import random

## AbstructBaseUser has provite some default field ( password, last_login, is_active )
class User(AbstractBaseUser, TimestampedModel, PermissionsMixin):

    class GenderType(models.TextChoices):
        MALE   = 'male'
        FEMALE = 'female'
        OTHER  = 'other'

    class UserRole(models.TextChoices):
        MEMBER   = 'member'
        MENTOR   = 'mentor'

    id        = models.UUIDField( primary_key = True, unique=True, default = uuid.uuid4, editable=False )
    email     = models.EmailField(
                    unique=True,
                    verbose_name="email address",
                    max_length=255,
                )
    phone     = models.CharField(
                    unique=True,
                    verbose_name="phone number",
                    max_length=30,
                    null=True, blank=True
                )
    name     = models.CharField(max_length=255, null=True, blank=True)
    gender   = models.CharField(max_length=10, choices=GenderType.choices, null=True, blank=True)
    dob      = models.DateField(null=True, blank=True) 

    profile_img    = models.ImageField(upload_to="ProfileImage/", null=True, blank=True)

    ## User Permission and Roll
    is_active   = models.BooleanField(default = True)
    is_admin    = models.BooleanField(default = False)
    is_verified = models.BooleanField(default = False)

    role = models.CharField(
        max_length = 10, 
        choices = UserRole.choices,
        null=True, blank=True
    )

    short_description = models.TextField(null= True, blank= True)
    description       = models.TextField(null= True, blank= True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        # return True      ## Default
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        # return True      ## Default
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'



class UserOTP(TimestampedModel):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    otp     = models.IntegerField()
    token   = models.CharField(max_length=100, null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"

    def generate_token(self):
        # generate 64 character token
        token = secrets.token_urlsafe(64)
        return token

    def generate_code(self):
        # generate 6 digit otp
        # otp = int(random() * 1000000)
        otp = random.randint(100000, 999999)
        return str(otp).zfill(6)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_code()

        if not self.token:
            self.token = self.generate_token()

        super().save(*args, **kwargs)

        
    


class Occupation(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_occupation')
    
    organization = models.CharField(max_length=225, null=True, blank=True)
    designation  = models.CharField(max_length=225, null=True, blank=True)
    
    def __str__(self):
        return self.organization
    



class Academic(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    roll       = models.CharField(max_length=225, null=True, blank=True)
    institute  = models.CharField(max_length=225, null=True, blank=True)
    department = models.CharField(max_length=225, null=True, blank=True)
    session    = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"{self.user.name}, {self.roll}" 
















