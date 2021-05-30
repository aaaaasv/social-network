from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


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

    def get_fields(self):
        fields = super(UserSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) in ['PUT', 'PATCH']:
            fields.pop('password')
            fields.pop('username')
        return fields


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'last_request')
        read_only_fields = ('id',)
