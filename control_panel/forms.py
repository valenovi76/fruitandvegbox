from django import forms

from .models import Newsletter


class NewsletterCreationForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = '__all__'
