# example/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from tongues_api.tongues_api import TonguesAPI
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from translation.models import ShareCode
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

@require_http_methods(["GET"])
def hero(request):

    # @TODO This method is called 'hero' as its only responsibility was to display the landing page, but
    # now I also added logic that checks whether a subodmain is passed in the url, and if so it redirects to the actual
    # application so it doesn't look very clean, and the naming or code structure needs to be changed
    host = request.get_host().split('.')
    
    if len(host) >= 2:
        subdomain = host[0]
    else:
        subdomain = None
        
    if subdomain:
        if ShareCode.objects.filter(code=subdomain).exists():
            return render(request, 'translation.html', {'share_code': ShareCode.objects.get(code=subdomain)})

    return render(request, 'hero/index.html')

@require_http_methods(["GET"])
def contact(request):
    return render(request, 'hero/contact.html')


@require_http_methods(["GET"])
def index(request):

    if not request.user.is_authenticated:
        messages.error(request, 'Login is required before you can use the application')
        return redirect('login')

    return render(request, 'translation.html')

@require_http_methods(["GET"])
def registration_page(request):
    return render(request, 'auth/registration.html')

@require_http_methods(["GET"])
def index_with_share_code(request, code):
    try:
        share_code = ShareCode.objects.get(code=code)

        if request.user.is_authenticated:
            if request.user != share_code.user:
                messages.success(request, "You have been logged out so you can utilize the share code.")
                logout(request)

        return render(request, 'translation.html', {'share_code': share_code})
    except ShareCode.DoesNotExist:
        messages.error(request, "Invalid share code.")
        return redirect('login')

@csrf_protect
@require_http_methods(["POST"])
def translate(request):
    base64 = request.POST.get('base64')
    source_lang = request.POST.get('source_lang')
    target_lang = request.POST.get('target_lang')

    tongues_api = TonguesAPI()

    try:
        status = 'success'
        status_code = 200
        res = tongues_api.translate_speech_to_speech(base64, source_lang, target_lang)
    except:
        status = 'fail'
        status_code = 500
        res = 'Something went wrong'

    return JsonResponse(
        {'status': status, 'translation_result': res}, status=status_code
    )