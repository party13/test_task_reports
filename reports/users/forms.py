import random
# from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


def create_random_pasword(length=6):
    alphabet= '2346789abcdefghkmnprstquxyzABCFEGTRPWKMNQ_'
    passw = ''
    for i in range(length):
        passw+=random.choice(alphabet)
    return passw


class RegisterForm(UserCreationForm):
    # username = forms.CharField(label='Username')
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, help_text="пароли должны совпадать")

    class Meta:
        model = User
        fields = ['username']
    #     help_text = {'username': 'используется для входа на сайт',
    #                  }
    #
    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords mismath!")
    #     return password2
    #
    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user
