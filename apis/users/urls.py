from django.urls import path

from apis.users import views

urlpatterns = [
    path("registration/", views.UserRegistrationView.as_view()),
    path("registration-verification/", views.UserRegistrationVerifyView.as_view()),
    path(
        "registration-verification-retry/",
        views.UserRegistrationVerify_retry_View.as_view(),
    ),
    path("login/", views.UserLoginView.as_view()),
    path("logout/", views.UserLogoutView.as_view()),
    path("profile/", views.UserProfileView.as_view()),
    path("forget-password-otp-send/", views.FP_OTPSendView.as_view()),
    path("forget-password-otp-verify/", views.FP_OTPVerificationView.as_view()),
    path("forget-password-set/", views.FP_PasswordSetView.as_view()),
    path("forget-password-otp-resend/", views.FP_OTPResendView.as_view()),
    path("change-password/", views.ChangePasswordView.as_view()),
]
