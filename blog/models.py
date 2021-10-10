from django.db import models
import os

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)

    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    #사용한 이미지 주소 (업로드할 경로, 필수는 아님)
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    #업로드한 파일 주소
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    #포스트한 날짜
    created_at = models.DateTimeField(auto_now_add=True)
    #사용자 지정이 아니라 포스트 생성시 자동으로 현재 시간, 날짜 데베에 저장
    updated_at = models.DateTimeField(auto_now=True)
    #author

    #각 object의 primarykey(id), title을 목록에 보여주는 함수
    def __str__(self):
        return f'[{self.pk}]{self.title}'

    # 각 상세 페이지로 이동 + 장고에 view on site 버튼
    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    # 업로드된 파일 이름 가져오기
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 업로드된 파일 확장자 가져오기
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]  # split 된 배열중 가장 마지막 요소가 확장자
