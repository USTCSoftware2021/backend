from django.urls import path
from . import views

app_name = 'cat'

urlpatterns = [
    path('index/', views.index, name='index'),
]
