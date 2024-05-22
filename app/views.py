import os
from django.http import HttpResponseBadRequest, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from app.rest_decorators import post_and_params_validator
import requests


@csrf_exempt
@post_and_params_validator(['text'])
def generate_test(request, data):
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


@csrf_exempt
@post_and_params_validator(['prompt'])
def generate_image(request, data):
    try:
        data = json.loads(request.body.decode('utf-8'))
        received_text = data.get('prompt')
        res = generate_image_request(received_text)
        return JsonResponse({'data': res})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON format in request body.')


def generate_image_request(prompt: str, aspect_ratio='1:1'):
    pre_prompt = ''
    url = "https://api.limewire.com/api/image/generation"
    payload = {
        "prompt": f"{pre_prompt} {prompt}",
        "aspect_ratio": aspect_ratio
    }

    headers = {
        "Content-Type": "application/json",
        "X-Api-Version": "v1",
        "Accept": "application/json",
        "Authorization": f"Bearer {os.environ.get("LIME_TOKEN")}",
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    return data
