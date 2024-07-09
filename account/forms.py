from django import forms
from .models import User


def validate_password(password):
    if (len(password) < 5):
        raise forms.ValidationError("Password must be 5 to 35 characters long")
    if (not (password.isalnum() and not password.isalpha() and not password.isdigit())):
        raise forms.ValidationError("Password must be alphanumeric")


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField()
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField()
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    password = forms.CharField(
        max_length=35,
        widget=forms.PasswordInput,
        validators=[validate_password],
        help_text="Password must be alphanumeric and 5 to 35 characters long."
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, }),
        required=False,
        max_length=500,
        help_text="Maximum length of 500 characters.")

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name',
                  'middle_name', 'last_name', 'date_of_birth', 'bio']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=['%d/%m/%Y', '%d-%m-%Y']
    )

    class Meta:
        model = User
        fields = ['profile_photo', 'first_name', 'middle_name', 'last_name',
                  'bio', 'date_of_birth', ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 7, }),
        }
