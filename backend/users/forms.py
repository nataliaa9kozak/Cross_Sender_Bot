from .models import CustomUser
from django import forms
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.validators import validate_email, EmailValidator
from django.core.exceptions import ValidationError
import logging


logger = logging.getLogger('django')


class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True, 'type': 'email', 'class': 'form-control'}),
        required=True,
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
        required=True,
    )

    field_order = ['email', 'password']

    def get_user(self):
        return CustomUser.objects.get(email=self.cleaned_data['email'])

    def get_authenticated_user(self):
        return authenticate(email=self.cleaned_data['email'], password=self.cleaned_data['password'])

    def is_valid(self):
        valid = super(CustomLoginForm, self).is_valid()
        if not valid:
            return valid

        try:
            user: CustomUser = self.get_user()
        except CustomUser.DoesNotExist:
            self.add_error('email', 'User with this email does not exist')
            return False

        if not user.check_password(self.cleaned_data['password']):
            self.add_error('password', 'Wrong password')
            return False

        return True


class CustomRegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
        required=True,
        min_length=3,
        max_length=50,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'}),
        required=True,
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
        required=True,
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
        required=True,
    )

    field_order = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError('Invalid email')

            return email
        raise ValidationError('User with this email already exists')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                'The two password fields didn\'t match.',
                code="password_mismatch",
            )
        return password2

    def get_user(self):
        return CustomUser.objects.get(email=self.cleaned_data['email'])

    def get_authenticated_user(self):
        return authenticate(email=self.cleaned_data['email'], password=self.cleaned_data['password1'])

    def is_valid(self):
        valid = super(CustomRegisterForm, self).is_valid()
        if not valid:
            return valid
        # proper password validation
        # try:
        #     password_validation.validate_password(self.cleaned_data['password1'])
        # except ValidationError as e:
        #     self.add_error('password1', e)
        #     return False

        password1 = self.cleaned_data.get("password1")
        if len(password1) < 5:
            self.add_error('password1', 'Password must be at least 5 characters long')
            return False

        return True

    def save(self, commit=True):
        user: CustomUser = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        if commit:
            user.save()
        return user
