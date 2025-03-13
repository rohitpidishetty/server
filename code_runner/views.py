import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
import sys
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def average_typing_speed(content):
  start = content[0]
  end = content[len(content)-1]
  start_time = start['timeStamp']
  end_time = end['timeStamp']
  total_time = end_time - start_time
  context = end['inputValue']
  word_count = len(context.split())
  return round(((total_time / word_count) / 1000), 2)
  
def context_jumps(content):
  print('--------')
  print(content)
  jumps = []
  initial_content = content[0]
  for cntxt_idx in range(1, len(content)):
    secondary_content = content[cntxt_idx]
    diff = (secondary_content['textLength'] - initial_content['textLength'])
    if diff not in [0, 1]:
      # print(diff)
      if diff < 0:
        json_context = {
          'before_edit': initial_content['inputValue'],
          'after_edit': secondary_content['inputValue'],
          'chars_deleted': diff
        }
        jumps.append(json_context)
      elif diff > 2:
        json_context = {
          'before_edit': initial_content['inputValue'],
          'after_edit': secondary_content['inputValue'],
          'chars_added': diff
        }
        jumps.append(json_context)
    initial_content = secondary_content
  return jumps

@csrf_exempt
def run(request):
  if request.method == "POST":
    body = json.loads(request.body)
    payload = body.get('code', [])
    try:
      code = payload[len(payload)-1].get('inputValue')
      output = io.StringIO()
      sys.stdout = output 
      exec(code)
      result = output.getvalue()
      sys.stdout = sys.__stdout__
      speed = average_typing_speed(content=payload)
      jumps = context_jumps(payload)
      print(jumps)
      return JsonResponse({"code": 200, "result": result.strip().replace('\n', '<br>'), "speed": speed, "context_jumps":jumps, "payload":payload})
    except Exception as e:
      return JsonResponse({"code": 404, "error": str(e)})
  return JsonResponse({"code": 500})

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_KEY")

@csrf_exempt
def mail(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        payload = body.get('report', {})
        final_edits = payload.get('edits', [])
        final_code = payload.get('code', '')
        user = payload.get('user', '')
        time = payload.get('time', '')
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = 'rohitpidishetty@gmail.com'
            msg["Subject"] = f'Code Journey by {user}'

            message = f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f9;
                            margin: 0;
                            padding: 20px;
                            color: #333;
                        }}
                        .container {{
                            max-width: 600px;
                            background-color: #ffffff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            margin: auto;
                        }}
                        h2 {{
                            color: #4CAF50;
                            text-align: center;
                        }}
                        .info {{
                            margin-bottom: 15px;
                            padding: 10px;
                            background-color: #f9f9f9;
                            border-left: 4px solid #4CAF50;
                        }}
                        pre {{
                            background-color: #eee;
                            padding: 10px;
                            border-radius: 5px;
                            overflow-x: auto;
                            white-space: pre-wrap;
                            word-wrap: break-word;
                        }}
                        .footer {{
                            text-align: center;
                            color: #999;
                            font-size: 12px;
                            margin-top: 20px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>Code Journey</h2>
                        <div class="info">
                            <strong>User:</strong> {user}
                        </div>
                        <div class="info">
                            <strong>Time:</strong> {time}
                        </div>
                        <div class="info">
                            <strong>Edits:</strong>
                            <ul>
                                {"".join(f"<li>{edit}</li>" for edit in final_edits)}
                            </ul>
                        </div>
                        <div class="info">
                            <strong>Code:</strong>
                            <pre>{final_code}</pre>
                        </div>
                        <div class="footer">
                            This is an auto-generated email. Please do not reply.
                        </div>
                    </div>
                </body>
            </html>
            """

            msg.attach(MIMEText(message, "html"))

            # Send email
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, 'rohitpidishetty@gmail.com', msg.as_string())
            server.quit()

            return JsonResponse({"status": 200})

        except Exception as e:
            return JsonResponse({"status": 400, 'err': str(e)})

    return JsonResponse({"status": 200})
