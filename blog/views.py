from django.contrib.auth import (
    authenticate,
    login,
    logout)
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect)
from django.utils import timezone
from .models import Post
from .forms import PostForm, UserForm


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'post-list.html', {'posts': posts})


def post_draft(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by(
        'created_date')
    return render(request, 'post-draft-list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post-detail.html', {'post': post})


def post_new(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                # post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'post-edit.html', {'form': form})


def post_edit(request, pk):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                # post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'post-edit.html', {'form': form})


def post_remove(request, pk):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.filter(
                    published_date__lte=timezone.now()).order_by(
                    'published_date')
                return render(request, 'post-list.html', {'posts': posts})
            else:
                return render(
                    request,
                    'login.html',
                    {'error_message': 'Your account has been disabled'}
                )
        else:
            return render(
                request,
                'login.html',
                {'error_message': 'Invalid login'}
            )
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'login.html', context)
