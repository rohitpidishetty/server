from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from getstream import Stream
import os

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

        
        
        name = mail[:mail.index('@')].strip()
        client = Stream(api_key=API_KEY, api_secret=API_SECRET, timeout=3.0)
        token = client.create_token(user_id=f"{name}-id")
        file = open('./approval.txt', 'r')
        status = file.read().strip()  # Assuming a static value for approval status; adjust as needed
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
