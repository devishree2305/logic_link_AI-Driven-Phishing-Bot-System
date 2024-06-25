"""
URL configuration for ai_phishing_bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# ai_phishing_bot/urls.py

from django.shortcuts import redirect
from django.urls import path, include
from campaigns import urls as campaigns_urls  # Importing 'urls' from 'campaigns' app

urlpatterns = [
    path('campaign/', include(campaigns_urls)),  
    path('', lambda request: redirect('campaign/')),  
    path('', lambda request: redirect('campaign_upload_csv')),
    path('', lambda request: redirect('campaign_add_campaign')),

]