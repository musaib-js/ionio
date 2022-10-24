from importlib.metadata import files
from msilib.schema import File
from rest_framework import serializers
from .models import User, Files


class UserRegistration(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['id', 'email', 'password']

class FileSerializer(serializers.ModelSerializer):
     class Meta:
        model = Files
        fields = ['file', 'uploaded_by']

class FileSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['file', 'created_at']