from django.urls import path
from . import views

urlpatterns = [
    path('generate_test/', views.generate_test, name='generate_test'),
    path('generate/', views.generate_image, name='generate'),
    path('generate_image/', views.generate_image_response, name='generate_image_response'),
    # Add more URL patterns as needed
]
