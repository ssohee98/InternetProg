from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag
from .forms import CommentForm



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

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST' :
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid() :
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else :
            return redirect(post.get_absolute_url())
    else :
        raise PermissionDenied

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        # 현재 사용자가 허락받은 사용자인가 테스트
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            # 비어있는 author instance에 현재 사용자 넣기
            form.instance.author = current_user

            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()  # 불필요한 공백 제거
                tags_str = tags_str.replace(',', ';')  # 모든 콤마를 세미콜론으로 변경
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:

            # 사용자 테스트 넘어가지 못한 경우 디폴트로 그냥 블로그 페이지 보여주기
            return redirect('/blog/')


class PostUpdate(LoginRequiredMixin, UpdateView):  # 모델명_form 템플릿 사용
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        # 로그인된 유저와 실제 작성자가 같으면
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists() :
            tags_str_list = list()
            for t in self.object.tags.all() :
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()  # 불필요한 공백 제거
            tags_str = tags_str.replace(',', ';')  # 모든 콤마를 세미콜론으로 변경
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response
   
class PostList(ListView):
    model = Post
    ordering = '-pk'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

    # template_name = 'blog/post_list.html'
    # post_list.html
    # 따로 템플릿 연결을 하지 않아도 클래스에 해당하는 html 이름으로 바꾸었으므로 자동으로 연결된다.

class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
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


