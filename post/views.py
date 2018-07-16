from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostModelForm

# Create your views here.
from .models import Post

def index(request):
	context = {'posts':Post.objects.all() }
	return render(request, 'post/index.html', context)

def details(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'post/details.html', {'post':post})

def create(request):
	form = PostModelForm(request.POST or None)
	if request.method == "POST":
		newPost = form.save(commit = False)
		newPost.save()
		return redirect('post:details', pk = newPost.id)

	return render(request, 'post/create.html', {'form':form})