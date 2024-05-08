#users/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import CustomUser
from .serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import UserRegistrationForm

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import logout

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


class UserLoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # 로그인 후 리다이렉션할 URL 패턴 이름
        else:
            error_message = "Invalid username or password."
            return render(request, self.template_name, {'error_message': error_message})

class UserRegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')  # 회원가입 후 리다이렉션할 URL 패턴 이름
        return render(request, self.template_name, {'form': form})

class UserProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'

    def get(self, request):
        user = request.user
        return render(request, self.template_name, {'user': user})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        next_url = request.GET.get('next', '/')
        return redirect(next_url)

    def post(self, request):
        logout(request)
        return redirect('index')