from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from getstream import Stream

API_KEY = 'sasejsckcqxg'
API_SECRET = '29wa6nxaw5bycfk96q45trrbbaz6bazujdecwcgj8jfkbrkuxw7emavamur36erm'


@csrf_exempt
def create_user(request):
    if request.method == 'GET':
        mail = request.GET.get('mail')
        if not mail:
            return JsonResponse({"error": "Email not provided."}, status=400)

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
            "approved": status
        })
        return response

    return JsonResponse({"status": 404})


def approval(request):
    if request.method == 'GET':
        file = open('./approval.txt', 'w')
        file.write(request.GET.get('status'))
        return JsonResponse({"state": request.GET.get('status')})
