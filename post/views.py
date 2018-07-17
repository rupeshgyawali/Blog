from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .forms import PostModelForm

# Create your views here.
from .models import Post

def index(request):
	paginator = Paginator(Post.objects.all(), 5)
	page = request.GET.get('page')
	context = {'posts': paginator.get_page(page) }
	return render(request, 'post/index.html', context)

def details(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'post/details.html', {'post':post})

def create(request):
	form = PostModelForm(request.POST or None)
	if request.method == "POST":
		if form.is_valid():
			newPost = form.save(commit = False)
			newPost.save()
			return redirect('post:details', pk = newPost.id)

	return render(request, 'post/create.html', {'form':form})


def edit(request, pk):
	instance = get_object_or_404(Post, pk = pk)
	form = PostModelForm(request.POST or None, instance = instance)
	if request.method == "POST":
		if form.is_valid:
			post = form.save(commit=False)
			post.save()
			return redirect('post:details', pk = post.id)

	return render(request, 'post/edit.html', {'form': form})


def delete(request, pk):
	post = get_object_or_404(Post, pk= pk)
	post.delete()
	return redirect('post:index')