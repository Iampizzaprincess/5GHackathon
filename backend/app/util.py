from flask import make_response

def check_req_fields(fields, obj):
    missing = [i for i, field in enumerate(fields) if field not in obj]
    return missing

def wrap_response(package):
    resp = make_response(package)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp