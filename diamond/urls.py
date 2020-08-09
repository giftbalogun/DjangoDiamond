from django.urls import path, include
from diamond import views

urlpatterns = [
    path('', views.index, name='index'),
]
