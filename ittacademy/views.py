from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from getstream import Stream
import os
import json
import firebase_admin
from firebase_admin import credentials, db

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
FIREBASE  =  json.loads(os.getenv("FIREBASE_PRIVATE_KEY"))

@csrf_exempt
def create_user(request):
    if request.method == 'GET':
        mail = request.GET.get('mail')
        if not mail:
            return JsonResponse({"error": "Email not provided."}, status=400)

        cred = credentials.Certificate(FIREBASE)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://itt-academy-default-rtdb.firebaseio.com/' 
        })
        ref = db.reference('/')
        status = ref.get('approval')
        name = mail[:mail.index('@')].strip()
        client = Stream(api_key=API_KEY, api_secret=API_SECRET, timeout=3.0)
        token = client.create_token(user_id=f"{name}-id")
        file = open('./approval.txt', 'r')
        status = file.read().strip()  
        response = JsonResponse({
            "user": name, 
            "token": token, 
            "user_id": f'{name}-id', 
            "api": API_KEY, 
            "approved": status
        })
        return response

    return JsonResponse({"status": 404})


def approval(request):
    if request.method == 'GET':
        file = open('./approval.txt', 'w')
        file.write(request.GET.get('status'))
        return JsonResponse({"state": request.GET.get('status')})
