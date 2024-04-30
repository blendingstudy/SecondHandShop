# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # 추가 필드 예시
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # 이메일 필드를 '필수' 및 '유니크' 값으로 설정
    email = models.EmailField(unique=True)

    # 필요한 경우 여기에 추가 메서드를 정의할 수 있습니다.
    # 예를 들어, 유저의 전체 이름을 반환하는 메서드
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username
