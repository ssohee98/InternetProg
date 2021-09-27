from django.shortcuts import render
from .models import Post

# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-pk')  # 최근 생성된 순서대로 모두 출력

    return render(request, 'blog/index.html',  # 사용할 템플릿
                  {
                      'posts': posts
                  }
                  )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)  # pk 값만 가져오기

    return render(request, 'blog/single_post_page.html',  # 사용할 템플릿
                  {
                      'post': post
                  }
                  )



