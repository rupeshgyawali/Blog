from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PostModelForm, LoginForm, RegisterForm, UserProfileModelForm
from .models import Post, UserProfile
from django.db.models import Q

def home(request):
	return redirect('post:index')

def profile(request, pk):
	profile = get_object_or_404(UserProfile, pk=pk)
	posts = profile.user.post_set.published()
	context = {'profile':profile, 'posts':posts}
	if request.user == profile.user:
		form = UserProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
		if request.method == 'POST':
			if form.is_valid:
				instance = form.save(commit=False)
				instance.save()
		posts = profile.user.post_set.all()
		context = {'profile':profile, 'form':form, 'posts':posts}
	return render(request, 'post/profile.html', context)

@login_required(login_url="post:login")
def follow(request, pk):
	user = request.user
	profile = get_object_or_404(UserProfile, pk=pk)
	if user != profile.user:
		user.userprofile.follows.add(profile)	
	return redirect('post:profile', pk=pk)


@login_required(login_url="post:login")
def unfollow(request, pk):
	user = request.user
	profile = get_object_or_404(UserProfile, pk=pk)
	if user != profile.user and profile in user.userprofile.follows.all():
		user.userprofile.follows.remove(profile)	
	return redirect('post:profile', pk=pk)

def index(request):
	queryset = Post.objects.published()
	msg = ''
	if request.user.is_authenticated:
		queryset = queryset.exclude(author=request.user)
		following_posts = queryset.filter(
			author__in = request.user.userprofile.follows.all().values_list('user',flat=True)
			)
		if not request.GET:
			queryset = following_posts
		elif request.GET.get('post') == 'allpost':
			queryset = queryset
			paginator = Paginator(queryset, 5)
			page = request.GET.get('page')
			context = {'posts': paginator.get_page(page),'msg':msg}
			return render(request, 'post/index.html', context)
		elif request.GET.get('search'):
			queryset = queryset.filter(
				Q(content__icontains = request.GET.get('search')) |
				Q(title__icontains = request.GET.get('search')) |
				Q(author__username = request.GET.get('search'))	|
				Q(author__first_name__icontains = request.GET.get('search')) |
				Q(author__last_name__icontains = request.GET.get('search'))
				).distinct()
			if not queryset:
				msg = 'No search result Found.'

	context = {'posts': queryset,'msg':msg}
	return render(request, 'post/index.html', context)

def details(request, slug):
	post = get_object_or_404(Post, slug=slug)
	if post.draft:
		if request.user != post.author and not request.user.is_authenticated:
			raise Http404
	return render(request, 'post/details.html', {'post':post})


@login_required(login_url="post:login")
def create(request):
	form = PostModelForm(request.POST or None, request.FILES or None)
	if request.method == "POST":
		if form.is_valid():
			newPost = form.save(commit = False)
			newPost.author = request.user
			newPost.save()
			messages.success(request, 'Post Created.')
			return redirect('post:details', slug = newPost.slug)

	return render(request, 'post/create.html', {'form':form})


@login_required(login_url="post:login")
def edit(request, pk):
	instance = get_object_or_404(Post, pk = pk)
	if request.user != instance.author:
		return redirect('post:details', slug = instance.slug)
	form = PostModelForm(request.POST or None, request.FILES or None, instance = instance)
	if request.method == "POST":
		if form.is_valid:
			post = form.save(commit=False)
			post.save()
			messages.success(request, 'Post updated.')
			return redirect('post:details', slug = post.slug)

	return render(request, 'post/edit.html', {'form': form})

@login_required(login_url="post:login")
def delete(request, pk):
	post = get_object_or_404(Post, pk= pk)
	if request.user != post.author:
		return redirect('post:details', slug = post.slug)
	post.delete()
	messages.success(request, 'Post deleted.')
	return redirect('post:index')



def loginUser(request):
	form = LoginForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username=username, password = password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('post:index')
	return render(request, 'post/login.html', {'form':form})



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
	return render(request, 'post/register.html', {'form':form})

@login_required(login_url="post:login")
def logoutUser(request):
	logout(request)
	return redirect('post:index')