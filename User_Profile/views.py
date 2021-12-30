from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView, DetailView, UpdateView, CreateView
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


def home_page(request):
    return render(request, 'base_panel/home.html')


def about(request):
    return render(request, 'base_panel/about.html', {'name': 'About'})


def contact(request):
    return render(request, 'base_panel/contact.html')


@login_required(login_url='login')
def panel(request):
    return render(request, 'index.html')


class ClientCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = "page-register.html"
    success_message = "user created successfully"

    class UserRegisterFormHH(UserCreationForm):
        email = forms.EmailField()

        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']
    form_class = UserRegisterFormHH

    def form_valid(self, form):
        obj = form.save()
        ClientProfile(user_p=obj).save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('base-panel')


class WorkerCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = "page-register.html"
    success_message = "employee added successfully"

    class workerRegisterFormHH(UserCreationForm):
        email = forms.EmailField()

        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']
    form_class = workerRegisterFormHH

    def form_valid(self, form):
        obj = form.save()
        WorkerProfile(user_wp=obj).save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('base-panel')


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = ClientProfile
    template_name = "profile_update.html"
    success_message = "profile updated successfully"
    fields = ["name_p", "image_p", "address_p", "phone_p"]

    def get_object(self, queryset=None):
        a=ClientProfile.objects.filter(user_p=self.request.user)
        if a.count()!=0: a = ClientProfile.objects.filter(user_p=self.request.user).get()
        else: a = WorkerProfile.objects.filter(user_p=self.request.user).get()
        return a

    def get_success_url(self):
        return reverse('profile-update')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["UserProfile"] = self.model.objects.filter(user_p=self.request.user).get()
        return context

    def test_func(self):
        a=ClientProfile.objects.filter(user_p=self.request.user)
        if a.count()==0:
            self.model=WorkerProfile
            self.fields=["name_p", "image_p", "address_p", "phone_p", "time_available_wp", "role_wp"]

        profile = self.get_object()
        if profile.user_p == self.request.user:
            return True
        return False


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "base_panel/user_confirm_delete.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('base-home')