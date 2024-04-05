"""
URL configuration for LoRaWanRescue project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.urls import re_path 
from appexpress import views
urlpatterns = [
    re_path(r'^$',views.login),
    path("index/",views.index),
    path("show_message/",views.show_message),
    path("show_users/",views.show_users),
    path("show_map/",views.show_map),
    path("position/",views.position),
    path("show_gateway/",views.gateway),
    path("show_situation_map/",views.situation_map),
    path("show_management/",views.management),
    path("show_log/",views.log),
    path("user_api/",views.user_api),
    path('message_api/',views.message_api),
    path('gateway_api/',views.gateway_api),
    path('client_api/',views.client_api),
    path('weather_api/',views.weather_api),
    path('num_api/',views.num_api), 
    path('log_api/',views.handle_log),
    path('delete_message/',views.delete_message),
    path('delete_user/',views.delete_user),
    path('delete_client/',views.delete_client),
    path('delete_gateway/',views.delete_gateway),
    path('map_api/',views.map_api),
    path("send_message/",views.send_message),
    path("update_pwd/",views.update_pwd),
    path("test/",views.test),
    path("chat_api/",views.chat_api)
]
