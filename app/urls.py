from django.urls import path
from . import views

urlpatterns = [
    path('generate_test/', views.generate_test, name='generate_test'),
    path('generate/', views.generate_image, name='generate'),
    # Add more URL patterns as needed
]
