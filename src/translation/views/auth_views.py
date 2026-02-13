from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout as logout_user
from django.shortcuts import redirect
from django.urls import reverse
from translation.utils.stripe_utils import charge_user_for_unpaid_usage
from translation.models import Transaction
from django.core.paginator import Paginator
from translation.exceptions import MinimumChargeError

@csrf_protect
@login_required
@require_http_methods(["GET"])
def dashboard_page(request):
    return render(request, 'auth/dashboard.html', {
        'payment_methods': request.user.payment_profile.get
    })

@csrf_protect
@login_required
@require_http_methods(["GET"])
def setup_payment_method_page(request):
    return render(request, 'auth/payment-required.html')

def logout(request):
    logout_user(request)
    messages.success(request, 'You have been successfully logged out')
    return redirect(reverse('login'))

@csrf_protect
@login_required
def charge_yourself(request):
    try:
        charge_user_for_unpaid_usage(request.user)
    except MinimumChargeError:
        messages.success(request, 'We will charge you when you own us more than $0.50.')
    else:
        messages.success(request, 'You have been successfully charged')

    return redirect(reverse('dashboard'))

@login_required
def list_transactions(request):
    transactions_list = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(transactions_list, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'auth/transactions.html', {'page_obj': page_obj})