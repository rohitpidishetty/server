import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
import sys

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


@csrf_exempt
def mail(request):
  if request.method == 'POST':
    body = json.loads(request.body)
    payload = body.get('report', {})
    final_edits = payload.get('edits', [])
    final_code = payload.get('code', '')
    user = payload.get('user', [])
    time = payload.get('time', '')
    print(final_code)
    print(final_edits)
    print(user)
    print(time)
    
  return JsonResponse({"status": 200})