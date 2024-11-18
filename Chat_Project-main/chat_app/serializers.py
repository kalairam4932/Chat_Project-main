from rest_framework import serializers

# Create your serializers here

class UserIdSerializer(serializers.Serializer):
    userId = serializers.CharField() 