from django.contrib import messages
from django.shortcuts import render

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
        else:
            messages.warning(request,
                             "Sorry we did not find your email address in our record",
                             "alert alert-warning alert-dismissible")

    context = {
        'form': form,
    }
    template = "newsletters/unsubscribe.html"
    return render(request, template, context)
