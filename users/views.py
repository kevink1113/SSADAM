from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View, UpdateView
from django.views.generic import FormView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import View
from . import models, forms
import datetime
from django.db.models import F, Q
from posts import models as post_models
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from . import forms
from django.db.models import Count, Avg, Max, Min, Sum


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        print(form)

    def delete(self, request):
        pass


def UserDelete(request):
    try:
        user = request.user
        user.delete()
        return redirect('/')
    except Exception:
        print("Could not delete user.\n")


def About(request):
    return render(request, "users/about.html")

@login_required
def UserDetail(request, pk):
    user = models.User.objects.get(pk=pk)

    # per = user.user_permissions.all()
    # print("권한들: ", per)
    if user.mil_fin is not None and user.mil_start is not None and user.is_soldier is not None:
        date_left = user.mil_fin - datetime.date.today()
        mil_time = user.mil_fin - user.mil_start
        if date_left.days <= 0 or mil_time.days <= 0:
            print("Division by 0 방지")
            date_left = datetime.timedelta(days=1)
            mil_time = datetime.timedelta(days=1)

        user.mil_percentage = round(100 * (1 - date_left / mil_time), 2)
        user.mil_left_date = date_left.days

    recent_posts = post_models.Post.objects.filter(~Q(board="anon"), user=user).order_by('-created')[:5]

    return render(request, "users/user_detail.html",
                  {"user": user, "recent_posts": recent_posts, "today": datetime.date.today()})


def UserView(request):
    users = models.User.objects.filter(is_real=True).order_by("?")

    for user in users:
        # print(user.avatar)

        if user.mil_fin is not None and user.mil_start is not None and user.is_soldier is not None:
            date_left = user.mil_fin - datetime.date.today()
            mil_time = user.mil_fin - user.mil_start

            if date_left.days <= 0 or mil_time.days <= 0:
                print("Division by 0 방지")
                date_left = datetime.timedelta(days=1)
                mil_time = datetime.timedelta(days=1)

            user.mil_percentage = round(100 * (1 - date_left / mil_time), 2)
            user.mil_left_date = date_left.days

    notifications = post_models.Post.objects.filter(board="notice").order_by('-created')[:5]
    print("최근 공지: ", notifications)
    recent_posts = post_models.Post.objects.order_by('-created').exclude(board="notice")[:5]

    trending_posts = post_models.Post.objects.annotate(like_sum=Count('like_users') - Count('dislike_users')).order_by(
        '-like_sum', '-created')[:5]

    # trending_posts = post_models.Post.objects.annotate(like_sum=F('like') - F('dislike')).order_by('-like_sum')[:5]

    # recent_posts.annotate(comments_cnt=Count(comment_models.Comment))
    # trending_posts.annotate(comments_cnt=Count(comment_models.Comment))

    return render(request, "users/user_info.html",
                  {"users": users, "today": datetime.date.today(), "notifications": notifications,
                   "recent_posts": recent_posts,
                   "trending_posts": trending_posts})


"""
def UserView(request):
    rooms = models.User.objects.all()
    return render(request, "users/", {"rooms": rooms})
"""


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        # email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:about")

    # initial = {"first_name": "상원", "last_name": "강", "username": "kevink1113"}

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class UpdateProfileView(SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "avatar", "bio", "birthdate", "is_soldier", "mil_start", "mil_fin", "mil_address", "homepage", "github_id",
        "blog", "boj_id", "student_id", "is_real", "username", "last_name", "first_name", "phone", "address",
    )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["last_name"].widget.attrs = {"placeholder": "성"}
        form.fields["first_name"].widget.attrs = {"placeholder": "이름"}
        form.fields["username"].widget.attrs = {"placeholder": "아이디"}
        form.fields["bio"].widget.attrs = {"placeholder": "하고 싶은 말"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "생일 ex) 2000-11-13"}
        form.fields["is_soldier"].widget.attrs = {"placeholder": "군인인가?"}
        form.fields["is_real"].widget.attrs = {"placeholder": "실제 계정인가?"}

        form.fields["mil_start"].widget.attrs = {"placeholder": "입영일 ex) 2020-10-10"}
        form.fields["mil_fin"].widget.attrs = {"placeholder": "전역일 ex) 2022-10-10"}
        form.fields["mil_address"].widget.attrs = {"placeholder": "부대 주소"}
        form.fields["homepage"].widget.attrs = {"placeholder": "개인 홈페이지 주소"}

        form.fields["github_id"].widget.attrs = {"placeholder": "GitHub ID"}
        form.fields["blog"].widget.attrs = {"placeholder": "개인 Blog 주소"}
        form.fields["boj_id"].widget.attrs = {"placeholder": "백준 ID"}
        form.fields["student_id"].widget.attrs = {"placeholder": "학번"}
        form.fields["phone"].widget.attrs = {"placeholder": "전화번호 ex) 010-0000-0000"}
        form.fields["address"].widget.attrs = {"placeholder": "집 주소"}
        return form
    """
    def form_valid(self, form):
        try:
            # username = form.cleaned_data.get("username")
            img = form.cleaned_data.get("avatar")
            img.thumbnail((20, 20))
        except Exception:
            print("could not create thumbnail for ", form.cleaned_data.get("avatar"))
        return super().form_valid(form)
    """

class UpdatePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "users/update-password.html"
    success_message = "Password Changed"

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required()
def rank(request):
    """
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post(**form.cleaned_data)
            post.user = request.user
            post.save()
            return redirect('posts:list')
    else:
        form = PostForm()
    """
    users = models.User.objects.all()

    data_posts = []
    label_posts = []

    data_like = []
    label_like = []

    data_dislike = []
    data_sumlike = []
    for user in users:
        usr = post_models.Post.objects.filter(user=user)
        user_posts = usr.count()
        data_posts.append(user_posts)
        label_posts.append(user.username)
        # print(user.username, " : ", user_posts)
        user_like = usr.aggregate(
            like_sum=Count("like_users"))
        user_dislike = usr.aggregate(
            dislike_sum=Count("dislike_users"))
        # like2 = user_like.get(like_users)
        print(user, "=>", user_like, user_like['like_sum'], "-", user_dislike["dislike_sum"])

        data_sumlike.append(user_like['like_sum'] - user_dislike["dislike_sum"])
        data_like.append(user_like['like_sum'])
        data_dislike.append(user_dislike["dislike_sum"])
        label_like.append(user.username)

    # userlist, namelist = zip(sorted(zip(userlist, namelist)))
    data_sumlike, label_like, data_like, data_dislike = (list(t) for t in zip(
        *sorted(zip(data_sumlike, label_like, data_like, data_dislike), reverse=True)))

    # arr = post_models.Post.objects.filter(user_id=1).aggregate(Sum("like_users"))
    # arr2 = arr.get('like_users')
    # print("랭킹: ", userlist)
    # print("이름: ", namelist)
    context = {
        'label_posts': label_posts,
        'data_posts': data_posts,

        'label_like': label_like,
        'data_sumlike': data_sumlike,
        'data_like': data_like,
        'data_dislike': data_dislike,
    }
    # return render(request, 'core/post_create.html', context)
    return render(request, 'users/rank.html', context)
