from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'User Management'

    # 필요한 경우 ready() 메서드를 정의합니다.
    # def ready(self):
    #     # users 앱에 대한 시그널을 여기서 등록합니다.
    #     import users.signals
