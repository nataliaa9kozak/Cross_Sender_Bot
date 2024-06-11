from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from users.models import CustomUser
from .models import UserConfig
from .serializers import UserConfigGetSerializer, UserConfigCreateSerializer
from django.contrib.auth import authenticate, login


class UserConfigAPIView(APIView):
    def get(self, request: Request):
        telegram_id = request.query_params.get('telegram_id', None)
        if not telegram_id:
            return Response({'telegram_id': 'required'}, status=status.HTTP_400_BAD_REQUEST)

        user: CustomUser = CustomUser.get_by_telegram_id(telegram_id)
        configs = UserConfig.objects.filter(user__pk=user.pk)

        serialized_configs = UserConfigGetSerializer(configs, many=True)

        return Response(
            serialized_configs.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request):
        telegram_id = request.data.get('telegram_id', None)
        if not telegram_id:
            return Response({'telegram_id': 'required'}, status=status.HTTP_400_BAD_REQUEST)

        social_media = request.data.get('social_media', None)
        if not social_media:
            return Response({'social_media': 'required'}, status=status.HTTP_400_BAD_REQUEST)

        content = request.data.get('content', None)
        if not content:
            return Response({'content': 'required'}, status=status.HTTP_400_BAD_REQUEST)

        user: CustomUser = CustomUser.get_by_telegram_id(telegram_id)
        request.data['user_id'] = user.pk

        try:
            config = UserConfig.objects.get(social_media=social_media, user__pk=user.pk)
        except UserConfig.DoesNotExist:
            config = None

        if config:
            serializer = UserConfigCreateSerializer(config, data=request.data, partial=True)
        else:
            serializer = UserConfigCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
