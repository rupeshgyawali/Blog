from rest_framework import serializers

from post.models import Post

class PostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['title', 'content']

class PostListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['id','author', 'title', 'content']


class PostDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['title', 'slug', 'content']