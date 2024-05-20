from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')

class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User created:", user)
            login(request, user)
            return redirect('dashboard')
        print("Form errors:", form.errors)
        return render(request, 'register.html', {'form': form})
