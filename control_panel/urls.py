from django.conf.urls import url

from newsletter.views import control_newsletter

urlspatterns = [
    url('newsletter/', control_newsletter, name='control_newsletter'),
]