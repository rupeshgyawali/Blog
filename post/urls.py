from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:pk>/', views.details, name = 'details'),
	path('newpost/', views.create, name = 'create'),
]