from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from getstream import Stream
from getstream.models import UserRequest
import firebase_admin
from firebase_admin import credentials, db
import os

API_KEY = 'sasejsckcqxg'
API_SECRET = '29wa6nxaw5bycfk96q45trrbbaz6bazujdecwcgj8jfkbrkuxw7emavamur36erm'

@csrf_exempt
def create_user(request):
  if request.method == 'GET':
    mail = request.GET.get('mail')
    name = mail[:mail.index('@')].strip()
    client = Stream(api_key=API_KEY, api_secret=API_SECRET, timeout=3.0)
    token = client.create_token(user_id=f"{name}-id")
    approval_status = True
    return JsonResponse({"user": name, "token": token, "user_id": f'{name}-id', "api": API_KEY, "approved": approval_status})    
  return JsonResponse({"status": 404})
