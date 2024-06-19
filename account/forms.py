from django import forms
from .models import User


def validate_password(password):
    if (len(password) < 5):
        raise forms.ValidationError("Password must be 5 to 35 characters long")
    if (not (password.isalnum() and not password.isalpha() and not password.isdigit())):
        raise forms.ValidationError("Password must be alphanumeric")


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        help_text="Accepted date format: DD/MM/YYYY or DD-MM-YYYY"
    )
    password = forms.CharField(
        max_length=35,
        widget=forms.PasswordInput,
        validators=[validate_password],
        help_text="Alphanumeric & 5 to 35 characters"
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'middle_name', 'last_name',
                  'bio', 'date_of_birth']


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
