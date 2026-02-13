from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .utils import check_database_status, check_redis_status
from tongues_api.tongues_api import TonguesAPI

@login_required
@staff_member_required
def health_check(request):
    return JsonResponse({
        'db': check_database_status(),
        'redis': check_redis_status(),
        'tongues_api': TonguesAPI().get_health_status()
    })