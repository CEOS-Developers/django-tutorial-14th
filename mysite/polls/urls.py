from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path()인수: route, view, (kwargs), name
]