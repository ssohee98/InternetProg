from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post

# Create your views here.

# def index(request):
#     posts = Post.objects.all().order_by('-pk')  # 최근 생성된 순서대로 모두 출력
#
#     return render(request, 'blog/post_list.html',  # 사용할 템플릿
#                   {
#                       'posts': posts
#                   }
#                   )
#
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)  # pk 값만 가져오기
#
#     return render(request, 'blog/post_detail.html',  # 사용할 템플릿
#                   {
#                       'post': post
#                   }
#                   )

class PostList(ListView) :
    model = Post
    ordering = '-pk'
    # template_name = 'blog/post_list.html'
    # post_list.html
    # 따로 템플릿 연결을 하지 않아도 클래스에 해당하는 html 이름으로 바꾸었으므로 자동으로 연결된다.


class PostDetail(DetailView) :
    model = Post
    # template_name = 'blog/post_detail.html'
    # post_detail.html


