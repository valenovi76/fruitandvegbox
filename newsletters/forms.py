from django import forms
from crispy_forms.helper import FormHelper

from .models import NewsletterUser, Newsletter


class NewsletterUserSignUpForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_lebels = False

    class Meta:
        model = NewsletterUser
        fields = ['email']

        def clean_email(self):
            email = self.cleaned_data.get('email')

            return email


class NewsletterCreationForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ['subject', 'body', 'email', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        super().__init__(*args, **kwargs)
        placeholders = {
            'subject': 'Newsletter Title',
            'body': 'Newsletter Content',
            'email': 'Select recipients',
            'status': 'Newsletter Status',
        }
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
        self.fields[field].widget.attrs['placeholder'] = placeholder
        self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
        self.fields[field].label = False
