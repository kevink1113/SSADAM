from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View, FormView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from . import models, forms
from math import floor
from .forms import PostForm
from .models import Post
from users import mixins as user_mixins
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from datetime import datetime

from posts import models as post_models
from django.contrib import messages


class TrendingList(ListView, user_mixins.LoginRequiredMixin, PermissionRequiredMixin):
    """ PostList Definition """
    model = models.Post
    queryset = post_models.Post.objects.annotate(like_sum=Count('like_users') - Count('dislike_users')).order_by(
        '-like_sum', '-created')
    paginate_by = 20
    paginate_orphans = 0
    # ordering = "-created"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super(TrendingList, self).get_context_data(**kwargs)
        context['board'] = "trending"
        today = datetime.now()
        context['today'] = today
        notifications = Post.objects.filter(board="notice").order_by('-created')[:5]
        recent_posts = post_models.Post.objects.order_by('-created').exclude(board="notice")[:5]
        trending_posts = post_models.Post.objects.annotate(
            like_sum=Count('like_users') - Count('dislike_users')).order_by(
            '-like_sum', '-created')[:5]
        context['notifications'] = notifications
        context['recent_posts'] = recent_posts
        context['trending_posts'] = trending_posts
        return context


class AnonList(ListView, user_mixins.LoginRequiredMixin, PermissionRequiredMixin):
    """ PostList Definition """
    model = models.Post
    queryset = models.Post.objects.filter(board__exact="anon")
    paginate_by = 20
    paginate_orphans = 0
    ordering = "-created"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super(AnonList, self).get_context_data(**kwargs)
        context['board'] = "anon"

        today = datetime.now()
        context['today'] = today
        notifications = Post.objects.filter(board="notice").order_by('-created')[:5]
        recent_posts = post_models.Post.objects.order_by('-created').exclude(board="notice")[:5]
        trending_posts = post_models.Post.objects.annotate(
            like_sum=Count('like_users') - Count('dislike_users')).order_by(
            '-like_sum', '-created')[:5]
        context['notifications'] = notifications
        context['recent_posts'] = recent_posts
        context['trending_posts'] = trending_posts
        return context


class NoticeList(ListView, user_mixins.LoginRequiredMixin, PermissionRequiredMixin):
    """ PostList Definition """
    model = models.Post
    queryset = models.Post.objects.filter(board__exact="notice")
    paginate_by = 20
    paginate_orphans = 0
    ordering = "-created"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super(NoticeList, self).get_context_data(**kwargs)
        context['board'] = "notice"

        today = datetime.now()
        context['today'] = today
        notifications = Post.objects.filter(board="notice").order_by('-created')[:5]
        recent_posts = post_models.Post.objects.order_by('-created').exclude(board="notice")[:5]
        trending_posts = post_models.Post.objects.annotate(
            like_sum=Count('like_users') - Count('dislike_users')).order_by(
            '-like_sum', '-created')[:5]
        context['notifications'] = notifications
        context['recent_posts'] = recent_posts
        context['trending_posts'] = trending_posts
        return context


class FreeList(ListView, user_mixins.LoginRequiredMixin, PermissionRequiredMixin):
    """ PostList Definition """
    model = models.Post
    queryset = models.Post.objects.filter(board__exact="free")
    paginate_by = 20
    paginate_orphans = 0
    ordering = "-created"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super(FreeList, self).get_context_data(**kwargs)
        context['board'] = "free"

        today = datetime.now()
        context['today'] = today
        notifications = Post.objects.filter(board="notice").order_by('-created')[:5]
        recent_posts = post_models.Post.objects.order_by('-created').exclude(board="notice")[:5]
        trending_posts = post_models.Post.objects.annotate(
            like_sum=Count('like_users') - Count('dislike_users')).order_by(
            '-like_sum', '-created')[:5]
        context['notifications'] = notifications
        context['recent_posts'] = recent_posts
        context['trending_posts'] = trending_posts
        return context


class PostList(ListView, user_mixins.LoginRequiredMixin, PermissionRequiredMixin):
    # raise_exception = True
    # permission_required = 'post.view_post'
    """
    permissions = (
        ('can_')
    )
    """
    """ PostList Definition """
    model = models.Post
    paginate_by = 20
    paginate_orphans = 0
    ordering = "-created"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['board'] = "post"

        today = datetime.now()
        context['today'] = today
        notifications = Post.objects.filter(board="notice").order_by('-created')[:5]
        recent_posts = post_models.Post.objects.order_by('-created').exclude(board="notice")[:5]
        trending_posts = post_models.Post.objects.annotate(
            like_sum=Count('like_users') - Count('dislike_users')).order_by(
            '-like_sum', '-created')[:5]
        context['notifications'] = notifications
        context['recent_posts'] = recent_posts
        context['trending_posts'] = trending_posts
        return context


class PostDetail(DetailView, user_mixins.LoggedInOnlyView, PermissionRequiredMixin):
    raise_exception = True
    permission_required = 'post.view_post'
    """
    class Meta:
        permission_required = (
            ("view_post", "can view post"),
        )
    """
    """ PostDetail Definition """
    model = models.Post
    pk = models.Post.pk

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        # models.Post.objects.count()
        pk = self.kwargs['pk']
        page_idx = models.Post.objects.count() - pk
        page_idx = floor(page_idx / 5) + 1
        if page_idx <= 0:
            page_idx = 1

        # print("페이지 - ", page_idx)
        board = models.Post.objects.get(pk=pk)
        print("제목 =>", board.board)
        context['page_idx'] = page_idx

        notifications = Post.objects.filter(board="notice").order_by('-created')[:5]
        recent_posts = post_models.Post.objects.order_by('-created').exclude(board="notice")[:5]
        trending_posts = post_models.Post.objects.annotate(
            like_sum=Count('like_users') - Count('dislike_users')).order_by(
            '-like_sum', '-created')[:5]
        context['notifications'] = notifications
        context['recent_posts'] = recent_posts
        context['trending_posts'] = trending_posts

        return context


class SearchView(ListView, user_mixins.LoginRequiredMixin):
    """ SearchView Definition """

    def get(self, request):

        title = request.GET.get("title")

        form = forms.SearchForm(request.GET)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            user = form.cleaned_data.get("user")
            board = form.cleaned_data.get("board")

            filter_args = {}
            if title != "":
                filter_args["title__contains"] = title

            if user is not None:
                filter_args["user"] = user

            if board != '':
                filter_args["board"] = board

            qs = models.Post.objects.filter(**filter_args).order_by("-created")
            paginator = Paginator(qs, 20, orphans=0)
            page = request.GET.get("page", 1)

            posts = paginator.get_page(page)

            return render(
                request, "posts/search.html", {"form": form, "posts": posts, "board": board}
            )

        else:
            form = forms.SearchForm()

        return render(request, "posts/search.html", {"form": form})


@login_required
def LikePost(request, pk):
    post = models.Post.objects.get(pk=pk)
    # print(post)
    # 이미 비추천이 있다면 먼저 이를 취소한다.
    if request.user in post.dislike_users.all():
        post.dislike_users.remove(request.user)
    # 이미 추천 눌렀다면, 취소.
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    # 누른 적이 없다면 추가.
    else:
        post.like_users.add(request.user)
    # post = get_object_or_404(PostList, pk=pk)
    # if request.userin post.
    # return redirect(reverse("posts:detail", pk=pk))
    # return HttpResponse()
    return redirect('posts:detail', pk)
    # return reverse("posts:detail", kwargs={"pk": pk})


@login_required
def disLikePost(request, pk):
    post = models.Post.objects.get(pk=pk)
    # 이미 추천이 있다면 먼저 이를 취소한다.
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    # 이미 비추천 눌렀다면, 취소.
    if request.user in post.dislike_users.all():
        post.dislike_users.remove(request.user)
    # 누른 적이 없다면 추가.
    else:
        post.dislike_users.add(request.user)
    return redirect('posts:detail', pk)


@login_required()
def NewPost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post(**form.cleaned_data)
            post.user = request.user
            post.save()
            return redirect('posts:list')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    # return render(request, 'core/post_create.html', context)
    return render(request, 'posts/new_post.html', context)


@login_required()
def delete_post(request, post_pk):
    # print(f"Should delete {post_pk}")
    user = request.user
    try:
        post = models.Post.objects.get(pk=post_pk)
        if post.user.pk != user.pk:
            messages.error(request, "You can't delete that Post!!")
        else:
            models.Post.objects.filter(pk=post_pk).delete()
            messages.success(request, "Post Deleted!")
        return redirect(reverse("posts:list"))
    except models.Post.DoesNotExist:
        return redirect(reverse("core:home"))


@login_required()
def modify_post(request, post_pk):
    user = request.user
    try:
        post = models.Post.objects.get(pk=post_pk)
        if post.user.pk != user.pk:
            messages.error(request, "You can't delete that Post!!")
            return redirect('posts:detail', pk=post_pk)

        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = user
                post.save()
                return redirect('posts:detail', pk=post_pk)
        else:
            form = PostForm(instance=post)
        context = {'form': form}
        return render(request, 'posts/new_post.html', context)

    except models.Post.DoesNotExist:
        return redirect('posts:detail', pk=post_pk)


"""
from django.urls import reverse
return redirect(reverse("core:home"))
return reverse("users:detail", kwargs={"pk": self.pk})
"""
