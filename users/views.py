import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View
from json.decoder import JSONDecodeError
from django.conf  import settings

from users.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            id       = data['id']
            password = data['password']

            if User.objects.filter(id = id).exists():
                return JsonResponse({'message' : 'ID_ALREADY_EXIST'}, status = 409)
            
            if not id:
                return JsonResponse({'message' : 'INVALID_ID'}, status = 400)

            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')

            User.objects.create(
                id       = id,
                password = decoded_password,
            )

            return JsonResponse({'message':'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except JSONDecodeError:
            return  JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(id = data['id']).exists():
                return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status = 404)

            user = User.objects.get(id = data['id'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 401)
            
            token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({'token' : token}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)