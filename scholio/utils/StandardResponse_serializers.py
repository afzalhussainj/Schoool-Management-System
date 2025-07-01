from rest_framework import serializers

class StandarizedSuccessResponseSerializer(serializers.Serializer):
    status = serializers.CharField(default='Success')
    message = serializers.CharField()
    data = serializers.DictField()

class StandarizedErrorResponseSerializer(serializers.Serializer):
    status = serializers.CharField(default='Failure')
    message = serializers.CharField()
    details = serializers.DictField()
