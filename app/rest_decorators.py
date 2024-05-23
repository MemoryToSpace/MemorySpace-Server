from django.http import HttpResponseBadRequest
import json


def post_only(view_func):
    """
  A decorator that ensures the decorated view function only accepts POST requests.
  """

    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseBadRequest('This endpoint only accepts POST requests.')
        return view_func(request, *args, **kwargs)

    return wrapper


def post_and_params_validator(params):
    """
  A decorator that checks for required parameters in the request body (JSON format).

  Args:
      params (list): A list of strings representing the required parameter names.

  Returns:
      function: The decorated function.
  """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.method != 'POST':
                return HttpResponseBadRequest('This endpoint only accepts POST requests.')
            if request.content_type != 'application/json':
                return HttpResponseBadRequest('This endpoint only accepts JSON POST requests.')

            try:
                data = json.loads(request.body.decode('utf-8'))
                missing_params = [param for param in params if param not in data]
                if missing_params:
                    message = f'Missing required parameters in JSON body: {", ".join(missing_params)}'
                    return HttpResponseBadRequest(message)
                return view_func(request, data, *args, **kwargs)  # Pass data to the view
            except json.JSONDecodeError:
                return HttpResponseBadRequest('Invalid JSON format in request body.')

        return wrapper

    return decorator
