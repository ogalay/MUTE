from django.template import RequestContext
from django.urls import reverse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic.base import View, TemplateView
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, render_to_response
# from account.forms import ProfileForm
from django.urls import reverse_lazy
from django.views import generic

from account.models import CustomUser
from .forms import CustomUserCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm

    success_url = "/account/login/"

    template_name = 'signup.html'


class Login(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(Login, self).form_valid(form)


class LogoutView(View):

    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")


def user_list(request):
    try:
        users = CustomUser.objects.order_by('username')
        context = {
            "title": "ListUser",
            "users": users,
        }
        return render_to_response("user_list.html", context)
    except CustomUser.DoesNotExist:
        return HttpResponseNotFound("<h2>Users not found</h2>")


def profile(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        context = {
            "title": "Profile",
            "user": user,
        }
        if request.user.pk == user_id:
            return render_to_response("profile.html", context)
        else:
            return HttpResponseRedirect("/", RequestContext(request))
    except CustomUser.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")


def create_staff(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    if user.is_staff:
        user.is_staff = False
    else:
        user.is_staff = True
    user.save()
    return HttpResponseRedirect(reverse('account:user_list'), RequestContext(request))


