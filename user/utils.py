import json, re, jwt
from django.http import JsonResponse
from my_settings import SECRET_KEY, JWT_ALGORITHM
from user.models import User, Gender, Country

class SigninConfirm:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)
        try:
            if access_token:
                token_payload = jwt.decode(access_token, SECRET_KEY, JWT_ALGORITHM)
                user          = User.objects.get(id=token_payload['user-id'])
                request.user  = user
                return self.original_function(self, request, *args, **kwargs)
            return JsonResponse({'MESSAGE' : 'INCORRECT_USER_INFORMATION'}, status=400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'MESSAGE' : 'EXPIRED_TOKEN'}, status=401)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE' : 'INCORRECT_USER_INFORMATION'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INCORRECT_USER_INFORMATION'}, status=401)

