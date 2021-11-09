from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag


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

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        # 현재 사용자가 허락받은 사용자인가 테스트
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            # 비어있는 author instance에 현재 사용자 넣기
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else :
            # 사용자 테스트 넘어가지 못한 경우 디폴트로 그냥 블로그 페이지 보여주기
            return redirect('/blog/')

class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

    # template_name = 'blog/post_list.html'
    # post_list.html
    # 따로 템플릿 연결을 하지 않아도 클래스에 해당하는 html 이름으로 바꾸었으므로 자동으로 연결된다.


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    # template_name = 'blog/post_detail.html'
    # post_detail.html


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)  # 받은 slug값과 같으면 카테고리값을 가져옴
        post_list = Post.objects.filter(category=category)

    return render(request, 'blog/post_list.html',
                  {
                      'post_list': post_list,  # 카테고리 값이 같은 Post만 가져옴
                      'categories': Category.objects.all(),
                      'no_category_post_count': Post.objects.filter(category=None).count(),
                      'category': category
                  })


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)  # 받은 slug값과 같으면 태그값을 가져옴
    post_list = tag.post_set.all()  # 다대다관계 // Post.objects.filter(tags=tag) 다대일관계

    return render(request, 'blog/post_list.html',
                  {
                      'post_list': post_list,  # 카테고리 값이 같은 Post만 가져옴
                      'categories': Category.objects.all(),
                      'no_category_post_count': Post.objects.filter(category=None).count(),
                      'tag': tag
                  })
