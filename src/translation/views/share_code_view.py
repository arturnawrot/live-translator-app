from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from translation.models import ShareCode
from django.views import View
from django.core.exceptions import ValidationError

SUCCESS_URL = 'share-code-page'

class ShareCodeForm(forms.ModelForm):
    class Meta:
        model = ShareCode
        fields = ['code']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            try:
                share_code = ShareCode.objects.get(user=self.user)
                self.fields['code'].initial = share_code.code
            except ShareCode.DoesNotExist:
                pass

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if ShareCode.objects.filter(code=code).exclude(user=self.user).exists():
            raise ValidationError("This share code is already in use by another user.")
        return code
    
class ShareCodeView(LoginRequiredMixin, FormView):
    template_name = 'auth/share_codes.html'
    form_class = ShareCodeForm

    def get_object(self):
        share_code, created = ShareCode.objects.get_or_create(user=self.request.user)
        return share_code

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect(SUCCESS_URL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['share_code2'] = self.get_object()
        return context
    
class DeleteShareCodeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        share_code = ShareCode.objects.filter(user=request.user).first()
        if share_code:
            share_code.delete()
        return redirect(SUCCESS_URL)