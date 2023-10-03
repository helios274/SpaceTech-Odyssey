from django import forms
from .models import CustomUser


def validate_password(password):
    if (len(password) < 5):
        raise forms.ValidationError("Password must be 5 to 35 characters long")
    if (not (password.isalnum() and not password.isalpha() and not password.isdigit())):
        raise forms.ValidationError("Password must be alphanumeric")


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True)
    password = forms.CharField(
        max_length=35, widget=forms.PasswordInput, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'middle_name', 'last_name',
                  'bio', 'date_of_birth']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_photo', 'first_name', 'middle_name', 'last_name',
                  'bio', 'date_of_birth', ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 7, }),
        }
