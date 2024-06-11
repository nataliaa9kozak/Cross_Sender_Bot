from django.urls import path
from .views import user_profile_view, CustomUserRegisterAPIView, UserExistAPIView
from django.contrib.auth.views import logout_then_login


name = 'users'
urlpatterns = [
    path('profile/', user_profile_view, name='user_profile'),
    path('logout/', logout_then_login, name='logout'),

    # api
    path('api/register/', CustomUserRegisterAPIView.as_view(), name='api_register'),
    path('api/user-exist/', UserExistAPIView.as_view(), name='api_user_exist'),
]
