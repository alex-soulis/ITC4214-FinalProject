# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class ProfileForm(forms.ModelForm):
    """
    Existing form for user basics plus extra profile fields.
    """
    profile_phone = forms.CharField(required=False)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

class UserForm(forms.ModelForm):
    """
    Form for editing built-in User fields on the edit page.
    """
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

class UserProfileForm(forms.ModelForm):
    """
    Form for editing UserProfile fields (address, phone_number).
    """
    class Meta:
        model = UserProfile
        fields = ("address", "phone_number", "profile_photo")
