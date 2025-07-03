from rest_framework import serializers

class standarizedSuccessResponseSerializer(serializers.Serializer):
    status = serializers.CharField(default='Success')
    message = serializers.CharField()
    data = serializers.DictField()

class standarizedErrorResponseSerializer(serializers.Serializer):
    status = serializers.CharField(default='Failure')
    message = serializers.CharField()
    details = serializers.DictField()
