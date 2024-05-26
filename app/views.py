import os
from django.http import HttpResponseBadRequest, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from app.rest_decorators import post_and_params_validator
import requests
from openai import OpenAI, OpenAIError

# Initialize the OpenAI client with the API key
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=openai_api_key)

@csrf_exempt
@post_and_params_validator(['text'])
def generate_image_response(request, data):
    """
    This view function retrieves text from the 'text' variable in a JSON request body,
    sends it to OpenAI's image generation API, and returns the generated image URL.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        received_text = data.get('text')
        
        if not received_text or not isinstance(received_text, str):
            return HttpResponseBadRequest('The "text" field must be a non-empty string.')
        
        # Refine the prompt for better image generation
        refined_prompt = f"Create a detailed and visually stunning image based on the following description: {received_text}"
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=refined_prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        image_url = response['data'][0]['url']
        
        return JsonResponse({'input_text': received_text, 'image_url': image_url})
    
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON format in request body.')
    except OpenAIError as e:
        return HttpResponseBadRequest(f'OpenAI API error: {str(e)}')
    except Exception as e:
        return HttpResponseBadRequest(f'Unexpected error: {str(e)}')

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
@post_and_params_validator(['text'])
def generate_image(request, data):
    try:
        data = json.loads(request.body.decode('utf-8'))
        received_text = data.get('text')
        refined_prompt = f"Create a detailed and visually stunning image based on the following description: {received_text}"
        res = generate_image_request(refined_prompt)
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
