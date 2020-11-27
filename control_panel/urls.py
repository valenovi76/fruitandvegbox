from django.urls import path
from newsletters import views

urlpatterns = [

    path('newsletter/', views.control_newsletter, name='control_newsletter'),

    path('newsletter-list/', views.control_newsletter_list,
         name='control_newsletter_list'),
    path('newsletter/<int:newsletter_id>', views.control_newsletter_detail,
         name='control_newsletter_detail'),
    path('newsletter-edit/<int:newsletter_id>', views.control_newsletter_edit,
         name='control_newsletter_edit'),
    path('newsletter-delete/<int:newsletter_id>',
         views.control_newsletter_delete,
         name='control_newsletter_delete'),
]

