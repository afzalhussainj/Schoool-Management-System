from rest_framework import response

def JsonFormatedResponse(data,message,status_code ,status='success'):
    return response({
        'status':status,
        'data':data,
        'message':message
    },status=status_code)