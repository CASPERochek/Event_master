from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'LOGIN'
        })
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'ПАРОЛЬ'
        })
    )


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'LOGIN'
        })
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повтор пароля'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        labels = {
            'email': '',
            'first_name': '',
            'last_name': '',
        }
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
        }





# from django import forms
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import AuthenticationForm
#
#
# class LoginUserForm(AuthenticationForm):
#     username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'input-group mb-3 ml-1030 mt-21 form-control', 'placeholder': 'LOGIN'}))
#     password = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'input-group mb-3 ml-1030 mt-21 form-control', 'placeholder': 'ПАРОЛЬ'}))
#
#
# # TextInput
# # PasswordInput
# # EmailInput
#
# class RegisterUserForm(forms.ModelForm):
#     username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'input-group mb-3 ml-1030 mt-21 form-control', 'placeholder': 'LOGIN'}))
#     password = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'input-group mb-3 ml-1030 mt-21 form-control', 'placeholder': 'Пароль'}))
#     password2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'input-group mb-3 ml-1030 mt-21 form-control', 'placeholder': 'Повтор пароля'}))
#
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
#         labels = {
#             'email': '',
#             'first_name': '',
#             'last_name': '',
#         }
#         widgets = {
#
#             'email': forms.TextInput(attrs={'class': 'input-group mb-3 ml-1030 mt-21 form-control', 'placeholder': 'E-mail'}),
#             'first_name': forms.TextInput(attrs={'class': 'input-group mb-3 ml-1030 mt-21 form-control', 'placeholder': 'Имя'}),
#             'last_name': forms.TextInput(attrs={'class': 'input-group mb-3 ml-1030 mt-21 form-control', 'placeholder': 'Фамилия'}),
#         }
#
#
#
#         # def clean_password2(self):
#         #     cd = self.cleaned_data
#         #     if cd['password'] != cd['password2']:
#         #         raise forms.ValidationError("Пароли не совпадают!")
#         #     return cd['password2']
#         #
#         # def clean_email(self):
#         #     email = self.cleaned_data['email']
#         #     if get_user_model().objects.filter(email=email).exists():
#         #         raise forms.ValidationError("Такой E-mail уже существует!")
#         #     return email