from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .models import CustomUserModel
from .forms import CustomUserCreateForm

class SignUpView(generic.CreateView):
    model = CustomUserModel
    form_class = CustomUserCreateForm
    template_name = "registration/signup_page.html"
    success_url = reverse_lazy("login")