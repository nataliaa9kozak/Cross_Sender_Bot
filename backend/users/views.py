from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View
from .forms import CustomLoginForm, CustomRegisterForm
from django.http import HttpResponseRedirect
from .serializers import CustomUserRegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import CustomUser


@login_required()
def user_profile_view(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'users/profile.html', context)


class AbstractAuthenticationView(View):
    form_class = None
    template_name = None
    success_url = None

    def form_valid(self, form: CustomRegisterForm):
        try:
            user = form.get_user()
        except CustomUser.DoesNotExist:
            user = form.save()

        login(self.request, user, backend='common.models.EmailBackend')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return self.success_url

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, self.template_name, {'form': form})


class CustomUserRegisterAPIView(APIView):
    def post(self, request):
        serializer = CustomUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserExistAPIView(APIView):
    def get(self, request: Request):
        telegram_id = request.query_params.get('telegram_id', None)
        email = request.query_params.get('email', None)
        if not telegram_id and not email:
            return Response({'message': 'telegram_id or email is required'})

        telegram_id_exist = False
        email_exist = False
        if telegram_id:
            telegram_id_exist = CustomUser.is_telegram_id_exist(telegram_id)
        if email:
            email_exist = CustomUser.is_email_exist(email)

        return Response(
            {'telegram_id': telegram_id_exist, 'email_exist': email_exist},
            status=status.HTTP_200_OK
        )
