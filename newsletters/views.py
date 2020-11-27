from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template

from .models import NewsletterUser, Newsletter
from .forms import NewsletterUserSignUpForm, NewsletterCreationForm
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


def control_newsletter(request):
    form = NewsletterCreationForm(request.POST or None)

    if form.is_valid():
        instance = form.save()
        newsletter = Newsletter.objects.get(id=instance.id)
        if newsletter.status == "Published":
            subject = newsletter.subject
            body = newsletter.body
            from_email = settings.EMAIL_HOST_USER
            for email in newsletter.email.all():
                send_mail(subject=subject, from_email=from_email,
                          recipient_list=[email], message=body,
                          fail_silently=True)

    context = {
        "form": form,
    }
    template = './control_panel/control_newsletter.html'
    return render(request, template, context)


def control_newsletter_list(request):
    newsletters = Newsletter.objects.all()

    paginator = Paginator(newsletters, 1)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        "items": items,
        "page_range": page_range
    }
    template = "control_panel/control_newsletter_list.html"
    return render(request, template, context)


def control_newsletter_detail(request, newsletter_id):
    """ A view to show individual Newsletters """
    newsletter = get_object_or_404(Newsletter, pk=newsletter_id)

    context = {
        "newsletter": newsletter,
    }
    template = "control_panel/control_newsletter_detail.html"
    return render(request, template, context)


def control_newsletter_edit(request, newsletter_id):
    newsletter = get_object_or_404(Newsletter, pk=newsletter_id)

    if request.method == 'POST':
        form = NewsletterCreationForm(request.POST, instance=newsletter)

        if form.is_valid():
            newsletter = form.save()

            if newsletter.status == "Published":
                subject = newsletter.subject
                body = newsletter.body
                from_email = settings.EMAIL_HOST_USER
                for email in newsletter.email.all():
                    send_mail(subject=subject, from_email=from_email,
                              recipient_list=[email], message=body,
                              fail_silently=True)
            return redirect('control_panel:control_newsletter_detail',
                            pk=newsletter.id)

    else:
        form = NewsletterCreationForm(instance=newsletter)

    context = {
        "form": form,
    }

    template = 'control_panel/control_newsletter.html'

    return render(request, template, context)


@login_required
def control_newsletter_delete(request, newsletter_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    newsletter = get_object_or_404(Newsletter, pk=newsletter_id)
    newsletter.delete()
    messages.success(request, 'Newsletter deleted!')
    return redirect(reverse('control_panel/control_newsletter_list'))
