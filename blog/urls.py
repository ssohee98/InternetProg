from . import views
from django.urls import path

urlpatterns = [
    # path('', views.index),    # 서버IP/blog
    # path('<int:pk>/', views.single_post_page)    # 서버IP/blog/

    path('search/<str:q>/', views.PostSearch.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>', views.tag_page),
    path('category/<str:slug>', views.category_page),   # 서버IP/blog/category/slug
    path('<int:pk>/new_comment/', views.new_comment),
    path('<int:pk>/', views.PostDetail.as_view()),  # 뷰가 부르는 부분을 함수가 아니라 뷰 같은 클래스로
    path('', views.PostList.as_view()),
]