from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('newpost/', views.create, name = 'create'),
	path('account/profile/<int:pk>', views.profile, name = 'profile'),
	path('account/profile/<int:pk>/follow/', views.follow, name = 'follow'),
	path('account/profile/<int:pk>/unfollow/', views.unfollow, name = 'unfollow'),
	path('account/login/', views.loginUser, name = 'login'),
	path('account/register/', views.register, name = 'register'),
	path('account/logout/', views.logoutUser, name = 'logout'),
	path('<slug:slug>/', views.details, name = 'details'),
	path('<int:pk>/edit/', views.edit, name = 'edit'),
	path('<int:pk>/delete/', views.delete, name = 'delete'),
]