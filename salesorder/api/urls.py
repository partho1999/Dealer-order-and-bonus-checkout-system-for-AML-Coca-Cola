from django.urls import path
from api import views

urlpatterns = [
    path('order/', views.api_list),
    
]