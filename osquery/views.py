from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .settings import *
from .osqueryResponses import *
from .enroll import generate_node_key, validate_node_key, get_enrolled_nodes
from .alerts import check_alerts, update_elastic
import json
from copy import deepcopy


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

    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    address = request.META.get('REMOTE_ADDR')
    node_key = json_data.get('node_key')

    if not validate_node_key(address, node_key):
        return JsonResponse(FAILED_ENROLL_RESPONSE)

    return JsonResponse(TEST_SCHED_QUERY)


@csrf_exempt
def logger(request):

    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    address = request.META.get('REMOTE_ADDR')
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

    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    address = request.META.get('REMOTE_ADDR')
    node_key = json_data.get('node_key')

    if not validate_node_key(address, node_key):
        return JsonResponse(FAILED_ENROLL_RESPONSE)

    query = deepcopy(DIST_QUERY)
    query = check_alerts(address, query)

    if not len(query['queries']):
        return JsonResponse(EMPTY_RESPONSE)

    return JsonResponse(query)

@csrf_exempt
def distributed_write(request):

    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    address = request.META.get('REMOTE_ADDR')
    node_key = json_data.get('node_key')
    results = json_data.get('queries')
    if results:
        queries = results.keys()
    else:
        queries = []


    if not validate_node_key(address, node_key):
        return JsonResponse(FAILED_ENROLL_RESPONSE)

    with open(LOG_OUTPUT_FILE, 'a') as f:
        for query in queries:
            if results[query] and len(results[query][0]):

                result_type = query.split('|')[0]
                direction = query.split('|')[1]
                uid = query.split('|')[2]

                if result_type == 'alert':
                    print(results[query][0])
                    update_elastic(direction, uid, results[query][0])
                else:
                    for result in results[query]:
                        result['address'] = address
                        f.write(json.dumps(result) + '\n')

    return JsonResponse(EMPTY_RESPONSE)


@csrf_exempt
def alert(request):

    data = request.body.decode('utf-8')
    json_data = json.loads(data)
    src_ip = json_data.get('src_ip')
    src_port = json_data.get('src_port')
    dest_ip = json_data.get('dest_ip')
    dest_port = json_data.get('dest_port')
    uid = json_data.get('alert_uid')
    secret = json_data.get('secret')
    enrolled_nodes = get_enrolled_nodes()

    if not secret == LOGSTASH_SECRET or \
            (not src_ip in enrolled_nodes and not dest_ip in enrolled_nodes):
        return None

    from osquery.models import alerts

    alerts.objects.all().delete()

    alert = alerts(src_ip=src_ip, src_port=src_port, dest_ip=dest_ip, dest_port=dest_port, uid=uid)
    alert.save()

    print(alerts.objects.all())

    return JsonResponse(EMPTY_RESPONSE)
