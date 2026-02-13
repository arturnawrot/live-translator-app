from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from translation.models import Contact
from django import forms
from django.contrib import messages

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'company_name', 'company_size', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_size': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ContactView(View):
    form_class = ContactForm
    template_name = 'hero/contact.html'  # Update this to your template path

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The message has been successfully sent!")
            return redirect(reverse('contact'))  # Redirect to a success page
        return render(request, self.template_name, {'form': form})