from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from posts import models as post_models
from . import models
from django.contrib import messages


@login_required()
def new_comment(request, pk):
    """ New Comment View definition """
    # post = get_object_or_404(post_models, pk=pk)
    # post = models.Post.objects.get(pk=post_pk)
    try:
        post = post_models.Post.objects.get(pk=pk)
        comment = post.comments.create(content=request.POST.get('content'), post=post_models.Post.objects.get(pk=pk), user=request.user)
        return redirect('{}#comment_{}'.format(
            resolve_url('posts:detail', pk=pk), comment.id
        ))
        # return redirect('posts:detail', pk=pk)
    except post_models.Post.DoesNotExist:
        return redirect('posts:detail', pk=pk)


@login_required()
def delete_comment(request, pk):
    """ Delete Comment View definition """
    # post = get_object_or_404(post_models, pk=pk)
    # post = models.Post.objects.get(pk=post_pk)
    user = request.user
    try:
        comment = models.Comment.objects.get(pk=pk)
        if comment.user.pk != user.pk:
            messages.error(request, "You can't delete that Comment!!")
        else:
            models.Comment.objects.filter(pk=pk).delete()
            messages.success(request, "Comment Deleted!")
        return redirect('posts:detail', pk=comment.post_id)
    except models.Comment.DoesNotExist:
        return redirect('posts:detail', pk=pk)
