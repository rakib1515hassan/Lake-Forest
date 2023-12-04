from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Perform the default authentication
        user, validated_token = super().authenticate(request)

        print("-----------------")
        print("User =", user)
        print("validated_token =", validated_token)
        print("request =", request)
        print("-----------------")

        # Check if the token is blacklisted
        if BlacklistedToken.objects.filter(token=validated_token).exists():
            raise AuthenticationFailed('Token is blacklisted.')

        # Override the user's id with a numeric representation
        validated_token['user_id'] = str(user.id)

        return user

    

def JWTBlacklistedTokenCheck(refresh_token):
    if BlacklistedToken.objects.filter(token=refresh_token).exists():
        # return api_error('', status=422, message='Token is invalid.')
        print("---------------------------")
        print("Token check")
        print("---------------------------")
        return False
    else:
        return True