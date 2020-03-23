from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Button, Reset
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        # self.helper.form_action = reverse_lazy('register')
        self.helper.layout = Layout(
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name',
            Submit('submit', 'Sign up', css_class='btn btn-success mt-2'),
            Reset('reset', 'Reset', css_class='btn btn-danger mt-2'))


class UserRegisterUpdateForm(forms.ModelForm):
    # alaws to uptade forms thru inhareits models
    class Meta:
        model = User
        fields = ['username', 'email', 'last_name']


class UserProfileUpdateForm(forms.ModelForm):
    # alaws to uptade forms thru inhareits models
    class Meta:
        model = Profile
        fields = ['branch', 'image']

