from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .settings import *
from .osqueryResponses import *
from .enroll import generate_node_key, validate_node_key
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

    node_key = generate_node_key(address)
    response = ENROLL_RESPONSE
    response['node_key'] = node_key

    return JsonResponse(response)


@csrf_exempt
def config(request):

    address = request.META.get('REMOTE_ADDR')
    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    node_key = json_data.get('node_key')

    if not validate_node_key(address, node_key):
        return JsonResponse(FAILED_ENROLL_RESPONSE)

    return JsonResponse(TEST_SCHED_QUERY)


@csrf_exempt
def logger(request):

    address = request.META.get('REMOTE_ADDR')
    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    results = json_data.get('data')
    log_type = json_data.get('log_type')
    node_key = json_data.get('node_key')

    if not validate_node_key(address, node_key):
        return JsonResponse(FAILED_ENROLL_RESPONSE)

    if results and log_type == 'result':
        with open(LOG_OUTPUT_FILE, 'a') as f:
            for result in results:
                logs = result['snapshot']
                for log in logs:
                    log['address'] = address
                    f.write(json.dumps(log) + '\n')

    return JsonResponse(EMPTY_RESPONSE)


@csrf_exempt
def distributed_read(request):
    response = HttpResponse("distributed_read")
    return response


@csrf_exempt
def distributed_write(request):
    response = HttpResponse("distributed_write")
    return response


@csrf_exempt
def alert(request):
    response = HttpResponse("alert")
    return response
