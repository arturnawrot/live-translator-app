from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from translation.forms import LoginForm
from django.urls import reverse_lazy
from django.contrib import messages

class LoginView(View):
    form_class = LoginForm
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse_lazy('index'))  # Assuming you have a url named 'index'
        
        messages.error(request, 'Wrong login or password.')
        return render(request, self.template_name, {'form': form})