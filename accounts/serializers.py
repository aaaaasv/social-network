from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ""),
            first_name=validated_data.get('first_name', ""),
            last_name=validated_data.get('last_name', "")
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
