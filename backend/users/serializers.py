from rest_framework import serializers
from .models import CustomUser


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'telegram_id')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data.get(
                'password', str(validated_data['telegram_id'])
            ),
            telegram_id=validated_data['telegram_id'],
        )

        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        return user
