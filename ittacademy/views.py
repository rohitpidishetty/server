from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from getstream import Stream
import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase import db

API_KEY = 'sasejsckcqxg'
API_SECRET = '29wa6nxaw5bycfk96q45trrbbaz6bazujdecwcgj8jfkbrkuxw7emavamur36erm'


@csrf_exempt
def create_user(request):
    if request.method == 'GET':
        mail = request.GET.get('mail')
        if not mail:
            return JsonResponse({"error": "Email not provided."}, status=400)
        
        TYPE = os.getenv("TYPE")
        PROJECT_ID = os.getenv("PROJECT_ID")
        PRIVATE_KEY_ID = os.getenv("PRIVATE_KEY_ID")
        PRIVATE_KEY = os.getenv("PRIVATE_KEY")
        CLIENT_EMAIL = os.getenv("CLIENT_EMAIL")
        CLIENT_ID = os.getenv("CLIENT_ID")
        AUTH_URI = os.getenv("AUTH_URI")
        TOKEN_URI = os.getenv("TOKEN_URI")
        AUTH_PROVIDER_X509_CERT_URL = os.getenv("AUTH_PROVIDER_X509_CERT_URL")
        CLIENT_X509_CERT_URL = os.getenv("CLIENT_X509_CERT_URL")
        UNIVERSE_DOMAIN = os.getenv("UNIVERSE_DOMAIN")

        service_acc_info = {
            "type": TYPE,
            "project_id": PROJECT_ID,
            "private_key_id": PRIVATE_KEY_ID,
            "private_key": PRIVATE_KEY,
            "client_email": CLIENT_EMAIL,
            "client_id": CLIENT_ID,
            "auth_uri": AUTH_URI,
            "token_uri": TOKEN_URI,
            "auth_provider_x509_cert_url": AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": CLIENT_X509_CERT_URL,
            "universe_domain": UNIVERSE_DOMAIN
        }

        cred = credentials.Certificate(service_account_info)
        # firebase_admin.initialize_app(cred, {
        #     'databaseURL': 'https://itt-academy-default-rtdb.firebaseio.com/' 
        # })
        # ref = db.reference('/')
        
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
            "approved": status,
            "test": UNIVERSE_DOMAIN
        })
        return response

    return JsonResponse({"status": 404})


def approval(request):
    if request.method == 'GET':
        file = open('./approval.txt', 'w')
        file.write(request.GET.get('status'))
        return JsonResponse({"state": request.GET.get('status')})
