from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostModelForm
from .models import Post
from profile.models import UserProfile
from django.db.models import Q

def home(request):
	return redirect('post:index')

def index(request):
	queryset = Post.objects.published()
	profiles = UserProfile.objects.all()
	if request.user.is_authenticated:
		profiles = UserProfile.objects.all().exclude(user=request.user)
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
			context = {'posts': paginator.get_page(page), 'profiles': profiles}
			return render(request, 'post/index.html', context)
		elif request.GET.get('search'):
			queryset = queryset.filter(
				Q(content__icontains = request.GET.get('search')) |
				Q(title__icontains = request.GET.get('search')) |
				Q(author__username = request.GET.get('search'))	|
				Q(author__first_name__icontains = request.GET.get('search')) |
				Q(author__last_name__icontains = request.GET.get('search'))
				).distinct()

	context = {'posts': queryset, 'profiles': profiles}
	return render(request, 'post/index.html', context)

def details(request, slug):
	post = get_object_or_404(Post, slug=slug)
	if post.draft:
		if request.user != post.author and not request.user.is_authenticated:
			raise Http404
	return render(request, 'post/details.html', {'post':post})


@login_required(login_url="profile:login")
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


@login_required(login_url="profile:login")
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

@login_required(login_url="profile:login")
def delete(request, pk):
	post = get_object_or_404(Post, pk= pk)
	if request.user != post.author:
		return redirect('post:details', slug = post.slug)
	post.delete()
	messages.success(request, 'Post deleted.')
	return redirect('post:index')

