from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from .models import Teacher, Student, User


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email,
                                   is_active=True).exists():
            raise ValidationError("There is no user registered \
                                  with the specified email address!")

        return email


class TeacherSignUpForm(UserCreationForm):
    '''
        Signup form for teachers
    '''
    email = forms.EmailField(max_length=254,
                             required=True,
                             help_text='Required. Input a valid email addresse')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name"]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("Email already exists!")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 2
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    '''
        Signup form for students
    '''
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'profile_image',
                  'email', 'residential_address',
                  'phone_number',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 1
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("Email already exists!")
        return email


class PostEmail(forms.Form):
    name = forms.CharField(max_length=35,
                           widget=forms.TextInput(attrs={'class': 'form-control-lg input-name', 'readonly':''})
                           )
    subject = forms.CharField(max_length=25,
                              widget=forms.TextInput(attrs={'class': 'form-control-lg', 'placeholder': 'difficulties... '})
                              )
    sender = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control-lg input-mailsender', 'readonly':''}))
    #receipient = forms.EmailField()
    message = forms.CharField(required=True, widget=forms.Textarea)
