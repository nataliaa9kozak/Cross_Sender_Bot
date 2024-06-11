from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, telegram_id=None, username=None):
        # if not email:
        #     raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(str(telegram_id) if telegram_id else password)
        user.telegram_id = telegram_id

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, username):
        user = self.create_user(
            email=email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    telegram_id = models.BigIntegerField(blank=True, null=True, unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @classmethod
    def is_telegram_id_exist(cls, telegram_id):
        return bool(cls.objects.get(telegram_id=telegram_id))

    @classmethod
    def is_email_exist(cls, email):
        return bool(cls.objects.get(email=email))

    @classmethod
    def get_by_telegram_id(cls, telegram_id):
        return cls.objects.get(telegram_id=telegram_id)

    def __str__(self):
        return self.email
