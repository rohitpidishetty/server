from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from getstream import Stream
import os
import json
import firebase_admin
from firebase_admin import credentials, db
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_KEY")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
FIREBASE  =  json.loads(os.getenv("FIREBASE_PRIVATE_KEY"))
cred = credentials.Certificate(FIREBASE)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://itt-academy-default-rtdb.firebaseio.com/' 
})
ref = db.reference('/')

@csrf_exempt
def create_user(request):
    if request.method == 'GET':
        mail = request.GET.get('mail')
        if not mail:
            return JsonResponse({"error": "Email not provided."}, status=400)
        status = ref.get('approval')[0].get('approval')
        name = mail[:mail.index('@')].strip()
        client = Stream(api_key=API_KEY, api_secret=API_SECRET, timeout=3.0)
        token = client.create_token(user_id=f"{name}-id")
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
        new_state = request.GET.get('status')
        state = {}
        try:
            ref.set({'approval':new_state})
            state = {"state": new_state}
        except Exception as e:
            state = {"state": "unchanged"}
        return JsonResponse(state)

@csrf_exempt
def purchase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            details = data['payload']['details']
            name = details['name']
            email = details['email']
            phone = details['phone']
            order = details['order']
            product = order['product']
            price = order['price']
            previous_price = order['previous_price']
            # try:
            #     message = f'NAME: {name}\nEMAIL: {email}\n PHONE: {phone}\nPRODUCT: {product}\nPRICE: {price}\nPREVIOUS PRICE: {previous_price}'
            #     msg = MIMEMultipart()
            #     msg["From"] = EMAIL_ADDRESS
            #     msg["To"] = 'rohitpidishetty@gmail.com'
            #     msg["Subject"] = f'Merchandise request by {name}'
            #     msg.attach(MIMEText(message, "plain"))
            #     server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            #     server.starttls()  # Secure connection
            #     server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Login
            #     server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())  # Send email
            #     server.quit()
            #     return JsonResponse({"status": 200})
            # except Exception as e:
            #     return JsonResponse({"status": 400, 'err': e})
        except Exception as e:
            return JsonResponse({"status": 400, 'err2': e})
        
