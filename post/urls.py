from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:pk>/', views.details, name = 'details'),
	path('newpost/', views.create, name = 'create'),
	path('<int:pk>/edit/', views.edit, name = 'edit'),
	path('<int:pk>/delete/', views.delete, name = 'delete'),
]