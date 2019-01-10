from django.urls import path, include
from . import views

app_name = 'post-api'

urlpatterns = [
	path('', views.PostListAPIView.as_view(), name='list'),
	path('<int:pk>/', views.PostDetailAPIView.as_view(), name = 'detail'),
	path('<int:pk>/edit/', views.PostUpdateAPIView.as_view(), name = 'edit'),
	path('<int:pk>/delete/', views.PostDeleteAPIView.as_view(), name = 'delete'),
	path('create/', views.PostCreateAPIView.as_view(), name = 'create'),
]