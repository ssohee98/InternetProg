from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),    # 서버IP/blog
    path('<int:pk>/', views.single_post_page)    # 서버IP/blog/
]