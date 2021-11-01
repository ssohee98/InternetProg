from . import views
from django.urls import path

urlpatterns = [
    # path('', views.index),    # 서버IP/blog
    # path('<int:pk>/', views.single_post_page)    # 서버IP/blog/

    path('category/<str:slug>', views.category_page),
    path('<int:pk>/', views.PostDetail.as_view()),  # 뷰가 부르는 부분을 함수가 아니라 뷰 같은 클래스로
    path('', views.PostList.as_view()),
]