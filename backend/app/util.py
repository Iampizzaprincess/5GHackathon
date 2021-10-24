from flask import make_response

def check_req_fields(fields, obj):
    missing = [field for field in fields if field not in obj.keys()]
    return missing

def wrap_response(package):
    resp = make_response(package)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'false'
    return resp