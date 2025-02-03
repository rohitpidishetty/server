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
            image = order['image']
            previous_price = order['previous_price']
            try:
                message = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    color: #0066cc;
                }}
                .content {{
                    margin-top: 20px;
                }}
                .content p {{
                    font-size: 16px;
                    line-height: 1.5;
                    margin: 8px 0;
                }}
                .footer {{
                    margin-top: 30px;
                    font-size: 14px;
                    text-align: center;
                    color: #888;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Merchandise Request</h2>
                </div>
                <div class="content">
                    <img src= 'https://itt-academy.web.app/merchandise/{image}' />
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Phone:</strong> {phone}</p>
                    <p><strong>Product:</strong> {product}</p>
                    <p><strong>Price:</strong> {price}</p>
                    <p><strong>Previous Price:</strong> {previous_price}</p>
                </div>
                <div class="footer">
                    <p>This is an automated message. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """

                msg = MIMEMultipart()
                msg["From"] = EMAIL_ADDRESS
                msg["To"] = 'rohitpidishetty@gmail.com'
                msg["Subject"] = f'Merchandise request by {name}'
                msg.attach(MIMEText(message, "html"))
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()  # Secure connection
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Login
                server.sendmail(EMAIL_ADDRESS, 'rohitpidishetty@gmail.com', msg.as_string())  # Send email
                server.quit()
                return JsonResponse({"status": 200})
            except Exception as e:
                return JsonResponse({"status": 400, 'err': e})
        except Exception as e:
            return JsonResponse({"status": 400, 'err2': e})
        
