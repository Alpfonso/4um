from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)

class ProfileForm(forms.Form):
    profile_description = forms.CharField(widget=forms.Textarea(attrs={
                'class':"form-control",
                'rows': 5,
                'style': 'width:60%',
                'placeholder': 'Write your profile description here!',
            }))