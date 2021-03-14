from django import forms
from . import models
from users import models as user_models
from .models import Post
from django_summernote.widgets import SummernoteWidget


class SearchForm(forms.Form):
    boardChoices = models.Post.BOARD_CHOICES
    boardChoices.insert(0, (None, '게시판 미정'))

    title = forms.CharField(initial="", required=False)
    user = forms.ModelChoiceField(
        required=False, empty_label="아무나", queryset=user_models.User.objects.all()
    )

    board = forms.ChoiceField(
        required=False, choices=boardChoices
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'board', 'content']
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "제목"}),
            'content': SummernoteWidget(),
        }
