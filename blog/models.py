from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
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