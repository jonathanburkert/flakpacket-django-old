from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def enroll(request):
    response = HttpResponse("enroll")
    return response


def config(request):
    response = HttpResponse("config")
    return response


def logger(request):
    response = HttpResponse("logger")
    return response


def distributed_read(request):
    response = HttpResponse("distributed_read")
    return response


def distributed_write(request):
    response = HttpResponse("distributed_write")
    return response


def alert(request):
    response = HttpResponse("alert")
    return response
