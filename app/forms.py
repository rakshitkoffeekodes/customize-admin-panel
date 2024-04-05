from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class RememberMeAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(label=_("remember me"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['remember_me'].widget.attrs.update({'class': 'checkbox'})

    def get_remember_me(self):
        print('=====', self.cleaned_data.get('remember_me'))
        return self.cleaned_data.get('remember_me')
