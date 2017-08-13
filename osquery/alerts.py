# alert functions

from osquery.models import alerts
from .osqueryResponses import *

def check_alerts(address, alert_query):

    src_alerts = alerts.objects.filter(src_ip=address)
    dest_alerts = alerts.objects.filter(dest_ip=address)

    for row in src_alerts:
        alert_query["queries"]["alert|src|" + row.uid] = PROC_PORT_QUERY.format(port=row.src_port)
    for row in dest_alerts:
        alert_query["queries"]["alert|dest|" + row.uid] = PROC_PORT_QUERY.format(port=row.dest_port)

    src_alerts.delete()
    dest_alerts.delete()

    return alert_query


def update_elastic(query, results):
    pass

    '''
    import elasticsearch, time

    es = elasticsearch.Elasticsearch(ES_CONN_STRING)
    direction = query.split('|')[1]
    alert_uid = query.split('|')[2]
    body = {"doc":{direction + "_cmdline": results["cmdline"], direction + "_pid": results["pid"]}}

    for i in (range(3)):
        alert = es.search(q="alert_uid: {}".format(alert_uid))
        if len(alert['hits']['hits']):
            alert = alert['hits']['hits'][0]
            es.update(index=alert['_index'], doc_type=alert['_type'], id=alert['_id'], body=body)
            break
        else:
            time.sleep(2)
    '''
