from django.db import models
from django.contrib.auth.models import User
import os

from markdown import markdown
from markdownx.models import MarkdownxField


# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=30)

    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()

    # 사용한 이미지 주소 (업로드할 경로, 필수는 아님)
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    # 업로드한 파일 주소
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    # 포스트한 날짜
    created_at = models.DateTimeField(auto_now_add=True)
    # 사용자 지정이 아니라 포스트 생성시 자동으로 현재 시간, 날짜 데베에 저장
    updated_at = models.DateTimeField(auto_now=True)

    # User에서 어떤 사용자가 삭제되면 그 사용자가 생성한 포스트도 모두 삭제
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    # User에서 어떤 사용자가 삭제되면 그 사용자가 생성한 포스트는 남도록
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)  # 다대다 관계

    # 각 object의 primarykey(id), title, 저자정보를 목록에 보여주는 함수
    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    # 각 상세 페이지로 이동 + 장고에 view on site 버튼
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    # 업로드된 파일 이름 가져오기
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 업로드된 파일 확장자 가져오기
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]  # split 된 배열중 가장 마지막 요소가 확장자

    def get_content_markdown(self):
        return markdown(self.content)

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/384/558d57b5d8a79409/svg/{self.author.email}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/384/558d57b5d8a79409/svg/{self.author.email}'