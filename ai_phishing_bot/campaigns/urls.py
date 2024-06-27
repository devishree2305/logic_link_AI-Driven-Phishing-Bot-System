from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='campaigns_index'),
    path('add_campaign/', views.add_campaign, name='add_campaign'), 
    path('upload_csv/', views.upload_csv, name='upload_csv'),
  
]
