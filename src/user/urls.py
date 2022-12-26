from django.urls import path, include
from .views import (UserListAPIView,
                    UserLoginView,
                    UserLogoutView,
                    UserRegisterView,
                    DetailUpdateView
                )


urlpatterns = [
    path('all-users', UserListAPIView.as_view()),
    path('login', UserLoginView.as_view()),
    path('logout', UserLogoutView.as_view()),
    path('register', UserRegisterView.as_view()),
    path('user/<int:pk>', DetailUpdateView.as_view()),
    
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
]
