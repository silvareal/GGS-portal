from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView,
                                  DeleteView,
                                  DetailView,
                                  ListView,
                                  UpdateView)
from django.contrib.admin.views.decorators import staff_member_required
from portal.decorators import teacher_required
from portal.forms import TeacherSignUpForm
from portal.models import User


@method_decorator([login_required, staff_member_required], name='dispatch')
class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('portal:portal-index')
