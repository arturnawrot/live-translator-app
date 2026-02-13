from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from translation.utils.stripe_utils import charge_user_for_unpaid_usage
from translation.exceptions import MinimumChargeError
from django.http import HttpResponseRedirect
from django.contrib import messages

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('index')  # Redirect after deletion

    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def delete(self, request, *args, **kwargs):
        """Call the extra method and then proceed with the user deletion."""
        self.object = self.get_object()
        
        try:
            charge_user_for_unpaid_usage(self.object, is_on_delete=True) 
        except MinimumChargeError:
            pass

        self.object.delete()  # Delete the object
        messages.success(request, 'Your account has been successfully deleted')
        return HttpResponseRedirect(self.get_success_url())  # Redirect after deletion

    def get(self, request, *args, **kwargs):
        """Handle GET requests: directly invoke delete."""
        return self.delete(request, *args, **kwargs)