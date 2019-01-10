from django.db.models import Q

from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
	RetrieveUpdateAPIView,
	)
from rest_framework.filters import OrderingFilter

from post.models import Post 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer

class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(author = self.request.user)


class PostListAPIView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	filter_backends = (OrderingFilter,)
	ordering_fields = ('title', 'author')

	def get_queryset(self, *args, **kwargs):
		queryset_list = super().get_queryset(*args, **kwargs)
		query = self.request.GET.get('search')
		if query:
			queryset_list = queryset_list.filter(
				Q(content__icontains = query) |
				Q(title__icontains = query) |
				Q(author__username = query)	|
				Q(author__first_name__icontains = query) |
				Q(author__last_name__icontains = query)
				).distinct()

		return queryset_list

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]