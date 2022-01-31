from django.urls import path
from .views import UserRegisterView, ProfileListAPIView, Logout,UserLoginView

urlpatterns = [
    path('register/',UserRegisterView.as_view()),
    path('login/',UserLoginView.as_view(),name="login_view"),
    path('logout/',Logout.as_view()),
    path('profile/',ProfileListAPIView.as_view()),
    # path('profile/<int:pk>/',ProfileUpdateDestroyAPIView.as_view()),
    ]