from django.conf import settings
from django.http import JsonResponse
from translation.models import User, UserProfile, Transaction
from django.db.models import Max
from django.utils import timezone
import datetime
from translation.utils.stripe_utils import charge_user_for_unpaid_usage
from translation.exceptions import MinimumChargeError

CRON_JOBS = [
    'cron_charge_everyone'
]

def cron_charge_everyone():
    users = User.objects.filter(is_superuser=False)

    for user in users:
        profile = UserProfile.objects.get(user=user)
        unpaid_duration = profile.total_unpaid_duration

        if unpaid_duration == 0:
            continue
        
        last_transaction = Transaction.objects.filter(user=user).aggregate(
            last_charged=Max('timestamp')
        )['last_charged']

        last_transaction = None

        if last_transaction:
            time_since_last_charge = timezone.now() - last_transaction

        if not last_transaction or time_since_last_charge > datetime.timedelta(days=1):
            payment_profile = user.payment_profile
            if payment_profile and payment_profile.has_payment_method:
                try:
                    charge_user_for_unpaid_usage(user)
                except MinimumChargeError:
                    continue 

def handle_cron(request):
    token = request.headers.get('CRON_AUTH_TOKEN')

    if token != settings.CRON_AUTH_TOKEN:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    cron_jobs = [globals()[name] for name in CRON_JOBS if name in globals()]

    for cron_job in cron_jobs:
        try:
            cron_job()
        except Exception as e:

            if settings.DEBUG:
                raise e

            print(str(e))
            pass

    return JsonResponse({'status': 'success'})