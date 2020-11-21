from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

from .models import NewsletterUser
from .forms import NewsletterUserSignUpForm
# Create your views here.


def newsletter_signup(request):
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request,
                             'Your Email Already Exists in our Records',
                             "alert alert-warning alert-dismissible")
        else:
            instance.save()
            messages.success(request,
                             "Your emails has been submitted successfully",
                             "alert alert-success alert-dismissible")
            subject = "Thank you for joining our Newsletter"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            with open(settings.BASE_DIR + "/newsletters/templates/newsletters/sign_up_email.txt") as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(subject=subject,
                                             body=signup_message,
                                             from_email=from_email,
                                             to=to_email)
            html_template = get_template("newsletters/sign_up_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()

    context = {
        'form': form,
    }
    template = "newsletters/sign_up.html"
    return render(request, template, context)


def newsletter_unsubscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request,
                             "Your email has been removed",
                             "alert alert-sucess alert-dismissible")
            subject = "You have been unsuscribed our Newsletter"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            with open(settings.BASE_DIR + "/newsletters/templates/newsletters/unsubscribe_email.txt") as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(subject=subject,
                                             body=signup_message,
                                             from_email=from_email,
                                             to=to_email)
            html_template = get_template("newsletters/unsubscribe_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()


        else:
            messages.warning(request,
                             "Sorry we did not find your email address in our record",
                             "alert alert-warning alert-dismissible")

    context = {
        'form': form,
    }
    template = "newsletters/unsubscribe.html"
    return render(request, template, context)
