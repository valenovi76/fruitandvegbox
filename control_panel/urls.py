from django.urls import path
from newsletters import views
from newsletters.views import control_newsletter, control_newsletter_list

urlpatterns = [
    path('newsletter/', views.control_newsletter, name='control_newsletter'),
    path('newsletter-list/', views.control_newsletter_list,
        name='control_newsletter_list'),
]