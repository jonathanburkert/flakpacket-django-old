# Enroll endpoint functions

def generate(address):

    record = None
    # Need to do DB lookup to see if node already
    # has a key

    if record:
        return record['node_key']
    else:
        node_key = str(random.randrange(1000000000, 9999999999))
        # Need to insert node_key / address into DB
        return node_key


def validate(address, node_key):
    return "validate"