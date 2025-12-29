from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

from .models import Profile

User = get_user_model()

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile_number', 'preferred_location', 'budget']
        widgets = {
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +919876543210'
            }),
            'preferred_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Hyderabad'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 5000000'
            }),
        }

class PasswordResetVerificationForm(forms.Form):
    """
    Form to verify the user's identity before allowing a password reset.
    """
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))

    def clean(self):
        """
        Custom validation to check if a user exists with the provided details.
        """
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')

        if first_name and last_name and email:
            try:
                # Case-insensitive check for all fields
                user = User.objects.get(
                    first_name__iexact=first_name,
                    last_name__iexact=last_name,
                    email__iexact=email
                )
                # Attach the user object to the form for use in the view
                self.user = user
            except User.DoesNotExist:
                raise forms.ValidationError("No account found with the provided details. Please check your information and try again.")
        return cleaned_data

class CustomSetPasswordForm(SetPasswordForm):
    """
    A custom password set form to apply Bootstrap styling.
    """
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )