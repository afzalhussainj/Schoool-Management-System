from rest_framework import response

def StandarizedSuccessResponse(data,message,status_code ,status='success'):
    return response({
        'status':status,
        'message':message,
        'data':data
    },status=status_code)

def StandarizedErrorResponse(details,message,status_code ,status=''):
    return response({
        'status':status,
        'message':message,
        'details':details
    },status=status_code)
