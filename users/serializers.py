from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=127, validators=[
        UniqueValidator(
            queryset=User.objects.all(), message="email already registered."
        )
    ])
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=150, validators=[
        UniqueValidator(
            queryset=User.objects.all(), message="username already taken."
        )
    ])
    password = serializers.CharField(max_length=128, write_only=True)
    birthdate = serializers.DateField(required=False)
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        if validated_data["is_employee"] is False:
            us = User.objects.create_user(**validated_data)
        else:
            us = User.objects.create_superuser(**validated_data)
        return us

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()
