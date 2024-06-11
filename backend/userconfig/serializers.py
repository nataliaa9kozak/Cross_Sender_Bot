from rest_framework import serializers
from .models import UserConfig


class UserConfigGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfig
        fields = (
            'content',
            'social_media',
        )


class UserConfigCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserConfig
        fields = (
            'content',
            'social_media',
            'user_id'
        )
