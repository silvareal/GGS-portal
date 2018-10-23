from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView
from portal.models import Student, Teacher, User
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail, get_connection
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from portal.forms import PostEmail
from portal.decorators import student_required, teacher_required
from portal.forms import EmailValidationOnForgotPassword


PasswordResetView.form_class = EmailValidationOnForgotPassword


class PortalIndex(TemplateView):
    template_name = 'portal/index.html'


class AboutView(TemplateView):
    template_name = 'aboutus.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.all()
        return context


class ContactView(TemplateView):
    template_name = 'contact.html'


# Get the student and teachers count
def student_count(request):
    # instance_list = User.objects.all()
    student_instance = User.objects.filter(user_type__contains=1).count()
    teacher_instance = User.objects.filter(user_type__contains=2).count()
    context = {
        'student_instance': student_instance,
        'teacher_instance': teacher_instance,
    }
    return render(request, 'index.html', context)

# Manin dashboard views
@login_required
def dashboard(request):
    # dashbord views
    return render(request, 'portal/dashboard.html')

@teacher_required
def add_update(request):
    # add student tables
    return render(request, 'portal/table-forms.html')

@teacher_required
def student_payment(request):
    # get the student payments Student payment views
    return render(request, 'portal/payment_table.html')


@login_required
def send_mail_to(request):
    # instance_list = User.objects.all()
    form = PostEmail(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            name_and_subject = f'{name} on {subject}'
            reciepients = ['admin@example.com']
            try:
                send_mail(name_and_subject,
                          message, sender,
                          reciepients,)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, f"Thanks <strong>{ request.user.first_name }</strong>, your message has been successfully sent", extra_tags='html_safe')
            return HttpResponseRedirect('')
    else:
        form = PostEmail()

    context = {
        'form': form,
    }

    return render(request, 'portal/mail-forms.html', context)
