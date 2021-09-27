from . import views
from django.urls import path

urlpatterns = [
    path('', views.landing),    # 서버IP/     # single_pages\views에 landing 함수
    path('about_me', views.about_me)    # 서버IP/about_me
]