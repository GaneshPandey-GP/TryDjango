from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, Http404
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from .models import Post
from .forms import PostForm


def create_post(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Successfully created!!")
            return redirect("/")

    contaxt = {"form": form}
    return render(request, 'create.html', contaxt)


def List_post(request):
    post = Post.objects.all().order_by('-timestamp')
    query = request.GET.get('q')
    if query:
        post = post.filter(Q(title__icontains=query) |
                           Q(content__icontains=query) |
                           Q(user__username__icontains=query)).distinct()

    paginator = Paginator(post, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginator_queryset = paginator.page(page)

    except PageNotAnInteger:
        paginator_queryset = paginator.page(1)

    except EmptyPage:
        paginator_queryset = paginator.page(paginator.num_pages)

    context = {"post": paginator_queryset, "title": 'List',
               'page_request_var': page_request_var}
    return render(request, 'index.html', context)


def details_post(request, slug):
    posts = Post.objects.get(slug=slug)
    context = {"posts": posts}
    return render(request, 'details.html', context)


def update_post(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    obj = Post.objects.get(slug=slug)
    form = PostForm(request.FILES or None, instance=obj)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated!!")
            return redirect("/")
    contaxt = {"form": form}
    return render(request, 'update.html', contaxt)


def delete_post(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    obj = Post.objects.get(slug=slug)
    if request.method == "POST":
        obj .delete()
        messages.success(request, "Successfully deleted !!")
        return redirect("/")

    contaxt = {"title": "Delete"}
    return render(request, 'delete.html', contaxt)
