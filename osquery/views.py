from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .settings import *
from .osqueryResponses import *
from . import enroll
import json

# Create your views here.

@csrf_exempt
def enroll(request):

    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    enroll_secret = json_data.get('enroll_secret')
    address = request.META.get('REMOTE_ADDR')

    if not enroll_secret or enroll_secret != ENROLL_SECRET:
        return JsonResponse(FAILED_ENROLL_RESPONSE)

    node_key = enroll.generate(address)
    response = ENROLL_RESPONSE
    response['node_key'] = node_key

    return JsonResponse(response)


def config(request):
    response = HttpResponse("config")
    return response


def logger(request):
    response = HttpResponse("logger")
    return response

@csrf_exempt
def distributed_read(request):
    response = HttpResponse("distributed_read")
    return response


def distributed_write(request):
    response = HttpResponse("distributed_write")
    return response

@csrf_exempt
def alert(request):
    response = HttpResponse("alert")
    return response
