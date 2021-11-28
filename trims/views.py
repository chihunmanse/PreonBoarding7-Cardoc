import json
import re

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from trims.models import Trim, Tire
from users.models import User, UserTrim
from trims.utils  import CardocAPI
from users.utils  import signin_decorator

class TrimView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if len(data) > 5:
                return JsonResponse({'message' : 'TOO_MUCH_REQUEST'}, status = 400)
            
            with transaction.atomic():
                for datum in data:
                    trim_data = CardocAPI().get_trim_data(datum['trimId'])
                    user      = User.objects.get(id = datum['id'])

                    if not trim_data:
                        return JsonResponse({'message' : 'INVALID_TRIM_ID'}, status = 400)
                    
                    trim_name       = trim_data['trimName']
                    front_tire_data = trim_data['spec']['driving']['frontTire']['value']
                    rear_tire_data  = trim_data['spec']['driving']['rearTire']['value']
                    TIRE_REGEX      = "\d+[/]\d+R\d+"

                    if not (re.compile(TIRE_REGEX).match(front_tire_data) and re.compile(TIRE_REGEX).match(rear_tire_data)):
                        return JsonResponse({'message' : 'INVALID_TIRE_FORMAT'}, status = 400)
                    
                    front_tire_values = re.split(r'[/,R]', front_tire_data)
                    rear_tire_values  = re.split(r'[/,R]', rear_tire_data)

                    front_tire, _ = Tire.objects.get_or_create(width = front_tire_values[0], aspect_ratio = front_tire_values[1], wheel_size = front_tire_values[2])
                    rear_tire, _  = Tire.objects.get_or_create(width = rear_tire_values[0], aspect_ratio = rear_tire_values[1], wheel_size = rear_tire_values[2])
                    trim, _       = Trim.objects.get_or_create(name = trim_name, front_tire = front_tire, rear_tire = rear_tire)

                    UserTrim.objects.get_or_create(user = user, trim = trim)
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'message' : "INVALID_USER_ID"}, status = 400)
    
    @signin_decorator
    def get(self, request):
        user   = request.user
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 10))
        
        trims = UserTrim.objects.select_related('trim__front_tire', 'trim__rear_tire').filter(user = user)[offset : offset + limit]

        data = [{
            'trim_name'  : trim.trim.name,
            'front_tire' : {
                'width'        : trim.trim.front_tire.width,
                'aspect_ratio' : trim.trim.front_tire.aspect_ratio,
                'wheel_size'   : trim.trim.front_tire.wheel_size,
            },
            'rear_tire' : {
                'width'        : trim.trim.rear_tire.width,
                'aspect_ratio' : trim.trim.rear_tire.aspect_ratio,
                'wheel_size'   : trim.trim.rear_tire.wheel_size,
            }, 
        }for trim in trims]

        return JsonResponse({'data' : data }, status = 200)





