from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
	path('<int:pk>', views.profile, name = 'profile'),
	path('<int:pk>/follow/', views.follow, name = 'follow'),
	path('<int:pk>/unfollow/', views.unfollow, name = 'unfollow'),
	path('login/', views.loginUser, name = 'login'),
	path('register/', views.register, name = 'register'),
	path('logout/', views.logoutUser, name = 'logout'),
]