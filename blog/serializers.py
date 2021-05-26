from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'id', 'text', 'author')
        read_only_fields = ('id', 'author')

    def create(self, validated_data):
        post = Post.objects.create(
            author=self.context['request'].user,
            text=validated_data['text'],
        )

        return post
