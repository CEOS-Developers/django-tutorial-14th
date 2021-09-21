from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 해당 url의 이름을 index로 설정
]