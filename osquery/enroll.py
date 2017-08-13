# Enroll endpoint functions
from osquery.models import enrolled_nodes
import random

def generate_node_key(address):

    record = enrolled_nodes.objects.filter(address=address)

    if record:
        return record[0].node_key
    else:
        node_key = str(random.randrange(1000000000, 9999999999))
        record = enrolled_nodes(address=address, node_key=node_key)
        record.save()
        return node_key


def validate_node_key(address, node_key):

    record = enrolled_nodes.objects.filter(address=address)

    if record and record[0].node_key == node_key:
        return True
    else:
        return False


def get_enrolled_nodes():

    return [row.address for row in enrolled_nodes.objects.all()]
