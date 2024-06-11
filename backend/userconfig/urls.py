from django.urls import path
from .views import UserConfigAPIView


name = 'userconfigs'
urlpatterns = [
    path('', UserConfigAPIView.as_view(), name='user_configs'),
]
