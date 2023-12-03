from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken

def JWTBlacklistedTokenCheck(refresh_token):
    if BlacklistedToken.objects.filter(token=refresh_token).exists():
        # return api_error('', status=422, message='Token is invalid.')
        print("---------------------------")
        print("Token check")
        print("---------------------------")
        return False
    else:
        return True