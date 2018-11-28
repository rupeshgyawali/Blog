from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, UserProfileModelForm
from .models import UserProfile
from django import forms


# Create your views here.
def profile(request, pk):
	profile = get_object_or_404(UserProfile, pk=pk)
	posts = profile.user.post_set.published()
	context = {'profile':profile, 'posts':posts}
	if request.user == profile.user:
		form = UserProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
		if request.method == 'POST':
			if form.is_valid():
				instance = form.save(commit=False)
				instance.save()
		posts = profile.user.post_set.all()
		context = {'profile':profile, 'form':form, 'posts':posts}
	return render(request, 'profile/profile.html', context)

@login_required(login_url="profile:login")
def follow(request, pk):
	user = request.user
	profile = get_object_or_404(UserProfile, pk=pk)
	if user != profile.user:
		user.userprofile.follows.add(profile)	
	return redirect('profile:profile', pk=pk)


@login_required(login_url="profile:login")
def unfollow(request, pk):
	user = request.user
	profile = get_object_or_404(UserProfile, pk=pk)
	if user != profile.user and profile in user.userprofile.follows.all():
		user.userprofile.follows.remove(profile)	
	return redirect('profile:profile', pk=pk)


def loginUser(request):
	form = LoginForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password = password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect(request.GET.get('next') or 'post:index')
			else:
				form.add_error(None, 'Invalid login or password. Please try again!')
	return render(request, 'profile/login.html', {'form':form})



def register(request):
	form = RegisterForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid:
			instance = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			instance.set_password(password)
			instance.save()
			user = authenticate(request, username=username, password = password)
			UserProfile.objects.create(user=user)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('post:index')
	return render(request, 'profile/register.html', {'form':form})

@login_required(login_url="profile:login")
def logoutUser(request):
	logout(request)
	return redirect('post:index')