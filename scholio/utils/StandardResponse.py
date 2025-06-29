from rest_framework import response

def StandarizedSuccessResponse(message,status_code ,data=None,status='Success'):
    return response({
        'status':status,
        'data':data,
        'message':message,
    },status=status_code)

def StandarizedErrorResponse(message,status_code ,details=None,status='Failure'):
    return response({
        'status':status,
        'message':message,
        'details':details
    },status=status_code)
