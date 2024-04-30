from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import CustomUser
from .serializers import UserSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# 사용자 목록을 보여주고 새로운 사용자를 생성하기 위한 뷰
class UserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    # 관리자만 사용자 목록에 접근할 수 있도록 설정
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]

# 개별 사용자의 상세 정보를 보여주고 수정 및 삭제를 처리하기 위한 뷰
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    # 해당 사용자 또는 관리자만 접근 가능하도록 설정
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })