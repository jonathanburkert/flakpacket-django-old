# OSQUERY RESPONSES

EMPTY_RESPONSE = {}

ENROLL_RESPONSE = {
    "node_invalid": False
}

FAILED_ENROLL_RESPONSE = {
    "node_invalid": True
}

TEST_SCHED_QUERY = {
    "schedule": {
        "test_query": {
            "query": "select * from processes;",
            "interval": 10,
            "snapshot": "true"
        }
    }
}

TEST_DIST_QUERY = {
    "queries": {
        "id1": "SELECT * FROM processes;"
    },
    "snapshot": "true"
}

DIST_QUERY = {
    "queries": {},
    "snapshot": "true"
}

PROC_PORT_QUERY = 'SELECT DISTINCT process.cmdline, process.pid FROM processes AS process JOIN process_open_sockets AS listening ON process.pid = listening.pid WHERE listening.local_port == {port} LIMIT 1;'