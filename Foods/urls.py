from django.contrib import admin
from django.urls import path, include

from Foods.views import get_food_info

app_name = 'Foods'

urlpatterns = [
    # 接口：下载文件
    path('<str:food_name>', get_food_info, name='get_food_info'),
]
