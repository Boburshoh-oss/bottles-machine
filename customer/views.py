from rest_framework import generics,views, permissions, response
from .serializers import UserLoginSerializer, UserRegisterSerializer,ProfileModelSerializer
from .models import User, Profile
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate
# Create your views here.
class UserRegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

# class UserLoginView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserLoginSerializer

class UserLoginView(views.APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        print(serializer,"data")
        return response.Response(serializer.data)


class Logout(views.APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return redirect("login_view")

class ProfileListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer
    
    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user)
        if profile[0].user.is_admin:
            profile = Profile.objects.all()
            return profile
        return profile