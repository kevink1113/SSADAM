from django import forms
from . import models


class LoginForm(forms.Form):
    """
    class Meta:
        model = models.User
        fields = ("username", "password")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "아이디"}),
        }
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ID'}))
    # email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        # email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            # user = models.User.objects.get(email=email)
            user = models.User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("username", forms.ValidationError("User does not exist"))
            # self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("last_name", "first_name", "username", "bio")
        widgets = {
            "last_name": forms.TextInput(attrs={"placeholder": "성"}),
            "first_name": forms.TextInput(attrs={"placeholder": "이름"}),
            "username": forms.TextInput(attrs={"placeholder": "닉네임"}),
            "bio": forms.TextInput(attrs={"placeholder": "하고 싶은 말"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"})
    )

    # password1 = forms.CharField(widget=forms.PasswordInput, label="비밀번호 확인")

    def clean_password1(self):
        """
        bio = self.cleaned_data.get("bio")
        validate = str(bio)
        if validate.__contains__("SGCS") is False:
            raise forms.ValidationError("You are not an authorized member of A.S.S.A!")
        """
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user.username = username
        user.set_password(password)
        user.save()
