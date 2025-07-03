from rest_framework.response import Response

def standarizedSuccessResponse(
        message,
        status_code ,
        data=(),
        status='Success'
        ):
    return Response({
        'status':status,
        'data':data,
        'message':message,
    },status=status_code)

def standarizedErrorResponse(
        message,
        status_code ,
        details={},
        status='Failure'
        ):
    return Response({
        'status':status,
        'message':message,
        'details':details
    },status=status_code)
