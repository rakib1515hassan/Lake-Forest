from django.template.loader import render_to_string
from apps.core.utils import html_mail_sender, sms_sender
from apps.users.models import UserOTP
from django.contrib.auth import get_user_model
User = get_user_model()

def OTP_Send(user, subject):
    try:
        user = User.objects.get(id=user.id)
        otp_obj = UserOTP.objects.filter(user=user).first()

        ## OTP Send On Email
        html_content = render_to_string('mail/forget_password_mail.html', {
            'user': user,
            'code': otp_obj.otp
        })

        html_mail_sender(
            subject,           ## subject
            html_content,      ## html_content
            [user.email],      ## to
        )
        
        ## OTP Send On Phone Number
        body = f"""
                    Welcome to Address PMS
                    Hi, {user.name}, 
                    Your verification OTP is {otp_obj.otp}

                    Regards,
                    Address PMS Team
            """
        sms_sender (
            user.phone,
            body,
        )

        return True

    except:
        return False
    