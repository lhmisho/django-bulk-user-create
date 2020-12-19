from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponse
from django.template import loader
# from django.contrib.auth import get_user_model
from django.conf import settings
# User = get_user_model()


def index(request):
    template = loader.get_template('create_user/index.html')
    context = {}
    return HttpResponse(template.render(context, request))