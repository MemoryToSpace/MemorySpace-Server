from django.http import HttpResponseBadRequest, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from app.rest_decorators import post_and_params_validator


@csrf_exempt
@post_and_params_validator(['text'])
def generate(request, data):
    """
  This view function retrieves text from the 'text' variable in a JSON request body and returns it.
  """
    # Parse the JSON body
    try:
        data = json.loads(request.body.decode('utf-8'))
        received_text = data.get('text')
        return JsonResponse({'text': received_text, 'image_url': 'https://ibb.co/CnqkkXM'})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON format in request body.')
