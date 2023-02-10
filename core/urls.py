from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/<int:number_of_requests>/', views.create_random_request, name='create_random_request'),
    path('summary/', views.summary, name='summary'),
    path('summary/json/', views.summary_json, name='summary_json'),
    path('last/<int:number_of_items>/', views.last_x, name='last'),
]
