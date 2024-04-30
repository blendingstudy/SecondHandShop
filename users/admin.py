from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# CustomUser 모델을 관리자 페이지에서 보기 좋게 설정
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # 사용자 목록에 표시될 필드 설정
    list_display = ['email', 'username', 'is_staff', 'phone_number']
    # 사용자 검색 필드 설정
    search_fields = ['email', 'username']
    # 사용자 편집 폼에서 필드 설정
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'profile_picture', 'address')}),
    )
    # 사용자 생성 폼에서 필드 설정
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'profile_picture', 'address')}),
    )

# CustomUser 모델을 Django 관리자에 등록
admin.site.register(CustomUser, CustomUserAdmin)
