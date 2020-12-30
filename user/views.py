import json, re, bcrypt, jwt, requests
from datetime         import datetime, timedelta
from django.shortcuts import redirect
from django.http      import JsonResponse
from django.views     import View
from user.models      import User, Gender, Country
from my_settings      import SECRET_KEY, JWT_ALGORITHM, CLIENT_ID, SECRET

REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '^[A-Za-z0-9~`!@#$%\^&*()-+=]{8,256}$'

class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            korean_name   = data['korean_name']
            english_name  = data['english_name']
            email         = data['email']
            phone_number  = data['phone_number']
            date_of_birth = data['date_of_birth']
            password      = data['password']
            gender        = data['gender']
            country       = data['country']
            gender_id     = Gender.objects.get(name=gender).id
            country_id    = Country.objects.get(name=country).id
            assert re.match((REGEX_EMAIL), email), 'INCORRECT_EMAIL_FORMAT'
            assert re.match((REGEX_PASSWORD), password), 'INCORRECT_PASSWORD_FORMAT'
            assert not User.objects.filter(email=email).exists(), 'ALREADY_EXISTS_EMAIL'
            assert not User.objects.filter(phone_number=phone_number).exists(), 'ALREADY_EXISTS_PHONE_NUMBER'
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                    korean_name   = korean_name,
                    english_name  = english_name,
                    email         = email,
                    phone_number  = phone_number,
                    date_of_birth = date_of_birth,
                    password      = hashed_password,
                    gender_id     = gender_id,
                    country_id    = country_id
                    )
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'BAD_REQUEST'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        except AssertionError as e:
            return JsonResponse({'MESSAGE' : f'{e}'}, status=401)

        except Gender.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'DOES_NOT_EXIST_GENDER'}, status=401)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            assert re.match((REGEX_EMAIL), data['email']), 'INCORRECT_EMAIL_FORMAT'
            assert User.objects.get(email=data['email']), 'INCORRECT_USER_INFORMATION'
            user = User.objects.get(email=data['email'])
            assert bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')), 'INCORRECT_USER_INFORMATION'

            payload          = {'user-id' : user.id, 'exp' : datetime.now() +timedelta(hours=1)}
            access_token     = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
            return JsonResponse({'access_token' : access_token}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'BAD_REQUEST'}, status=400)

        except AssertionError as e:
            return JsonResponse({'MESSAGE' : f'{e}'}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'DOES_NOT_EXIST_USER'}, status=401)

class KakaoSignInView(View):
    def post(self, request):
        access_token = request.headers.get('Authorization', None)
        response     = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization' : f'Bearer {access_token}'}).json()
        user_email   = response['kakao_account']['email']
        user_name    = response['kakao_account']['profile']['nickname']

        if User.objects.filter(email=user_email).exists():
            user    = User.objects.get(email=user_email)
            payload = {'user-id' : user.id, 'exp' : datetime.now() +timedelta(hours=1)}
            token   = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
            return JsonResponse({'access_token' : token}, status=200)
        return JsonResponse({
            'MESSAGE' : 'NOT_EXIST_USER',
            'EMAIL'   : user_email,
            'NAME'    : user_name,
            },status=403)
