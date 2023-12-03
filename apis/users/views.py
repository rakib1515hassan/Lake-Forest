from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
import random
from django.template.loader import render_to_string

from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
        IsAuthenticated, 
    )

from apps.users.models import UserOTP 
from apps.core.utils import (
    ApiBaseView, 
    api_success, 
    api_error, 
    create_JWT_token, 
    html_mail_sender, 
    sms_sender,
)
from rest_framework import serializers
from apis.users.Serializers.RegistrationSerializer import (
        UserRegistrationSerializer, 
        UserRegistrationVerifySerializer,
    )

from apis.users.Serializers.ForgetPasswordSerializer import (
    FP_OTPSendSerializer,
    FP_OTPVerificationSerializer,
    FP_PasswordSetSerializer,
    FP_OTPResendSerializer
)
from apis.users.Serializers.ChangeEmailandPhoneSerializer import (
    UserEmailChangeSerializer,
    UserPhoneChangeSerializer,
    Email_Change_OTPVerificationSerializer,
    Phone_Change_OTPVerificationSerializer
)

from apis.users.Serializers.ProfileSerializer import CustomerSerializer
from apis.users.Serializers.LoginSerializer import UserLoginSerializer

from apis.users.Serializers.ChangePasswordSerializer import UserChangePasswordSerializer

from apis.users.utils import OTP_Send
from django.contrib.auth import get_user_model
User = get_user_model()



"""
    User Registration
    @Rakib
"""
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        user_serializer = UserRegistrationSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()

            # Get the user by email
            user = User.objects.filter(email=user_serializer.validated_data['email']).first()
            otp  = UserOTP.objects.filter(user = user).first()
            if otp:
                msg = {
                    'token': otp.token, 
                    'message': 'Registration Successful. Please check your email.'}
                return api_success(user_serializer.data, status=201, message=msg)
            else:
                return api_error({'message': 'User not found'}, status=404)

        return api_error({'errors': user_serializer.errors}, status=422, message="Validation error!")
    



"""
    User Verify after registration
    @Rakib
"""
class UserRegistrationVerifyView(APIView):

    def post(self, request, format=None):
        serializer = UserRegistrationVerifySerializer(
                data = request.data, 
            )
        if serializer.is_valid():
            msg = {'Your account is verified. Now you can log in.'}
            return api_success(serializer.data, status=201, message=msg)
            
        return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
    


"""
    User Verify after registration (Resend OTP registration)
    @Rakib
"""
class UserRegistrationVerify_retry_View(APIView):
    def post(self, request, format=None):
        token = request.data.get('token')
        if token:
            try:
                old_otp = UserOTP.objects.get(token=token)
                try:
                    user = User.objects.get(id = old_otp.user.id)

                    if user is not None:
                        # UserOTP.objects.get(user = user).delete() ## Delete Old OTP

                        new_otp = UserOTP.objects.create(user=user) ## New OTP Create 
                        old_otp.delete()                            ## Delete Old OTP

                        html_content = render_to_string('mail/otp_mail.html', {
                            'user': user,
                            'code': new_otp.otp
                        })

                        html_mail_sender(
                            'Please verify your Account',  ## subject
                            html_content,                  ## html_content
                            [user.email],                  ## to
                        )
                        
                        # print("--------------------------------")
                        # print(f"Name= {user.name}, OTP= {new_otp.otp}, Token= {new_otp.token}")
                        # print("--------------------------------")

                        msg = {
                            'token': new_otp.token,
                            'message':'Once again OTP has been sent on your email or phone number.'
                        }
                        return api_success('', status=201, message=msg)
                    
                except User.DoesNotExist:
                    return api_error({'errors': 'Invalid User'}, status=400, message="Validation error!")

            except UserOTP.DoesNotExist:
                return api_error({'errors': 'Invalid token'}, status=400, message="Validation error!")

        else:
            return api_error({'token': 'Token is requered!'}, status=400, message="Validation error!")
    



"""
    User Login with Email or Phone Number
    @Rakib
"""
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email_or_phone = serializer.data.get('email_or_phone')
            get_user = User.objects.filter(Q(email=email_or_phone) | Q(phone=email_or_phone)).first()

            if get_user is not None:
                if get_user.is_verified == True:
                    login(request, get_user)       
                    token = create_JWT_token(get_user)   ## Token Genaret
                    msg = {
                        'token': token,
                        'message':'Login Success',
                        'user_id':get_user.id,
                        }
                    return api_success(serializer.data, status=201, message = msg)
                
                else:
                    # Delete previous otp if have
                    if UserOTP.objects.filter(user = get_user).first():
                        UserOTP.objects.filter(user = get_user).delete()

                    new_otp = UserOTP.objects.create(user = get_user)  ## Create new otp

                    # html_content = render_to_string('mail/otp_mail.html', {
                    #     'user': get_user,
                    #     'code': new_otp.otp
                    # })

                    # html_mail_sender(
                    #     'Please verify your Account',  ## subject
                    #     html_content,                  ## html_content
                    #     [get_user.email],                  ## to
                    # )
                    
                    # ## Phone varification
                    # body = f"""
                    #             Welcome to Address PMS
                    #             Hi, {get_user.name}, 
                    #             Thank you for registering with us. Please use the following code to verify your account.
                    #             Your verification OTP is {new_otp.otp}

                    #             Regards,
                    #             Address PMS Team
                    #     """
                    # sms_sender (
                    #     get_user.phone,
                    #     body,
                    # )

                    print("--------------------------------")
                    print(f"User Name : {get_user.name}, User Otp : {new_otp.otp}")
                    print("--------------------------------")

                    msg = {
                        'token': new_otp.token, 
                        'message': 'Please verify your account. Verification OTP send on your email or phone number.'
                    }
                    return api_error({'errors': serializer.errors}, status=422, message=msg)
            else:
                return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
                
        else:
            return api_error({'errors': serializer.errors}, status=422, message="Validation error!")




# """
#     User Logout 
#     @Rakib
# """
# class UserLogoutView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes     = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data.get("refresh_token")
#             if not refresh_token:
#                 return api_error({'errors': 'Refresh token is required'}, status=400, message='Invalid refresh token')

#             # Revoke the refresh token using Django's logout function
#             logout(request)

#             return api_success('', status=200, message='User successfully logged out.')

#         except Exception as e:
#             return api_error({'errors': str(e)}, status=400, message='Invalid refresh token')

# # class UserLogoutView(APIView):
# #     authentication_classes = [JWTAuthentication]
# #     permission_classes = [IsAuthenticated]

# #     def post(self, request):
# #         try:
# #             refresh_token = request.data.get("refresh_token")
# #             if not refresh_token:
# #                 return api_error({'errors': 'Refresh token is required'}, status=400, message='Invalid refresh token')

# #             token = RefreshToken(refresh_token)
# #             token.blacklist()

# #             # Assuming you are using Django's built-in logout function
# #             logout(request)

# #             return api_success('', status=200, message='User successfully logged out.')

# #         except Exception as e:
# #             return api_error({'errors': str(e)}, status=400, message='Invalid refresh token')




# """
#     Forget Password OTP send
#     @Rakib
# """
# class FP_OTPSendView(APIView):
#     serializer_class = FP_OTPSendSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})

#         if serializer.is_valid():
#             user = User.objects.filter(email=serializer.validated_data['email']).first()
#             otp = UserOTP.objects.filter(user = user).first()
#             if otp:
#                 msg = {
#                     'token': otp.token, 
#                     'message': 'OTP send successfully. Please check your email or phone to verify your account.'}
#                 return api_success(serializer.data, status=201, message=msg)
#             else:
#                 return api_error({'message': 'User not found'}, status=404)
                
#         return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
    



# """
#     Forget Password OTP verification
#     @Rakib
# """
# class FP_OTPVerificationView(APIView):
#     serializer_class = FP_OTPVerificationSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             msg = {'Verification is successful. Now you can set the password.'}
#             return api_success(serializer.data, status=201, message = msg)
        
#         return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
    



# """
#     Forget Password Password Reset
#     @Rakib
# """
# class FP_PasswordSetView(APIView):
#     serializer_class = FP_PasswordSetSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             msg = {'Password set successfully.'}
#             return api_success('', status=201, message = msg)
        
#         return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
    




# """
#     Forget Password Resend OTP
#     @Rakib
# """
# class FP_OTPResendView(APIView):

#     def post(self, request, format=None):
#         token = request.data.get('token')
#         if token is None:
#             return api_error({'errors': {'token':'token field is required!'}}, status=422, message="Validation error!")

#         try:
#             old_otp_obj = UserOTP.objects.get(token=token)
#             user = User.objects.filter(id = old_otp_obj.user.id).first()

#             serializer = FP_OTPResendSerializer(data=request.data)

#             if serializer.is_valid():
#                 new_otp_obj = UserOTP.objects.filter(user=user).first()

#                 # print("--------------------------------")
#                 # print(f"Name= {user.name}, OTP= {new_otp_obj.otp}, Token= {new_otp_obj.token}")
#                 # print("--------------------------------")

#                 msg = {
#                     'token': new_otp_obj.token,
#                     'message':'Once again OTP has been sent on your email or phone number.'
#                 }
#                 return api_success('', status=200, message=msg)
            
#             return api_error({'errors': serializer.errors}, status=422, message="Validation error!")

#         except UserOTP.DoesNotExist:
#             return api_error({'errors': 'Invalid token'}, status=400, message="Validation error!")



# """
#     Change Password 
#     @Rakib
# """
# class ChangePasswordView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes     = [IsAuthenticated]

#     def post(self, request, format=None):
#         serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
#         if serializer.is_valid():
#             msg = "Password is successfully changed."
#             return api_success('', status=200, message=msg)
            
#         return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
    



# """
#     Customer Update, Details and Delete View 
#     @Rakib
# """
# class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes     = [IsAuthenticated]
#     serializer_class = CustomerSerializer
#     queryset = User.objects.all()

#     def get(self, request, *args, **kwargs):
#         instance   = self.get_object()
#         serializer = self.get_serializer(instance)
#         msg = "User retrieved successfully!"
#         return api_success(serializer.data, status=200, message=msg)
        
#     def update(self, request, *args, **kwargs):
#         fields_to_check = ['email','phone','is_active','is_verified','is_admin','is_superuser','created_at' ,'user_type','auth_provider']

#         try:
#             instance = self.get_object()
#             serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))

#             if serializer.is_valid():
#                 for field in fields_to_check:
#                     if field in request.data:
#                         raise serializers.ValidationError(f"Cannot update the '{field}' field!")

#                 self.perform_update(serializer)
#                 msg = "User updated successfully!"
#                 return api_success(serializer.data, status=200, message=msg)
#             else:
#                 return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
#         except ValidationError as e:
#             return api_error({'errors': e.detail}, status=422, message="Validation error!")

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         msg = "User deleted successfully!"
#         return api_success({}, status=204, message=msg)

#     def perform_destroy(self, instance):
#         instance.delete()

#     # def handle_exception(self, exc):
#     #     # Customize the error response
#     #     if isinstance(exc, serializers.ValidationError):
#     #         return Response(api_error({'errors': exc.detail}, status=422, message="Validation error!"))
#     #     return super().handle_exception(exc)


#     # def get_queryset(self):
#     #     user = self.request.user
#     #     if user.is_staff:
#     #         return User.objects.all()
#     #     else:
#     #         return User.objects.filter(id=user.id)

    

# """
#     Customer Email Change ( OTP Send Email) 
#     @Rakib
# """
# class Email_Change_OTPSendView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes     = [IsAuthenticated]

#     def post(self, request, format=None):
#         user = request.user

#         if UserOTP.objects.filter(user = user).first(): ## Delete previous OTP
#             UserOTP.objects.get(user = user).delete()

#         otp_obj = UserOTP.objects.create(user = user)

#         serializer = UserEmailChangeSerializer(data=request.data, context = {
#             'user': user, 
#             'otp_obj': otp_obj, 
#             'request':request
#             })

#         if serializer.is_valid():
#             if otp_obj:
#                 print("--------------------------------")
#                 print(f"User Name : {user.name}, User Otp : {otp_obj.otp}")
#                 print("--------------------------------")
#                 msg = {
#                     'token': otp_obj.token, 
#                     'message': 'OTP send successfully.'}
#                 return api_success(serializer.data, status=200, message=msg)
#             else:
#                 return api_error({'message': 'User not found'}, status=404)

#         return api_error({'errors': serializer.errors}, status=422, message="Validation error!")

        



# """
#     Customer Email Change ( OTP Verification and New Email Set) 
#     @Rakib
# """
# class Email_Change_OTPVerificationView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes     = [IsAuthenticated]
#     serializer_class = Email_Change_OTPVerificationSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context = {
#             'user': request.user,
#             'request': request
#             })

#         if serializer.is_valid():
#             msg = {'Verification is successful. New Email is saved.'}
#             return api_success(serializer.data, status=201, message = msg)
        
#         return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
    




# """
#     Customer Phone Change ( OTP Send Phone) 
#     @Rakib
# """
# class Phone_Change_OTPSendView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes     = [IsAuthenticated]

#     def post(self, request, format=None):
#         user = request.user

#         if UserOTP.objects.filter(user = user).first(): ## Delete previous OTP
#             UserOTP.objects.get(user = user).delete()

#         otp_obj = UserOTP.objects.create(user = user)

#         serializer = UserPhoneChangeSerializer(data=request.data, context = {
#             'user': user, 
#             'otp_obj': otp_obj, 
#             'request':request
#             })

#         if serializer.is_valid():
#             if otp_obj:
#                 print("--------------------------------")
#                 print(f"User Name : {user.name}, User Otp : {otp_obj.otp}")
#                 print("--------------------------------")
#                 msg = {
#                     'token': otp_obj.token, 
#                     'message': 'OTP send successfully.'}
#                 return api_success(serializer.data, status=200, message=msg)
#             else:
#                 return api_error({'message': 'User not found'}, status=404)

#         return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
    



# """
#     Customer Phone Change ( OTP Verification and New Phone Set) 
#     @Rakib
# """
# class Phone_Change_OTPVerificationView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes     = [IsAuthenticated]
#     serializer_class = Phone_Change_OTPVerificationSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context = {
#             'user': request.user,
#             'request': request
#             })

#         if serializer.is_valid():
#             msg = {'Verification is successful. New Phone number is saved.'}
#             return api_success(serializer.data, status=201, message = msg)
#         else:
#             return api_error({'errors': serializer.errors}, status=422, message="Validation error!")