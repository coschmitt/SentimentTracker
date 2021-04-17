from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/tweets/auth_home")
    else:       # Unregistered User
        return HttpResponseRedirect("/tweets/sign-up")


class SignUp(FormView):
    success_url = "/tweets/auth_home"
    form_class = UserCreationForm
    template_name = "tweets/signup.html"

    def form_valid(self, form):
        form.save()
        user = User.objects.get(username=form.data.get('username'))
        login(self.request, user)
        form.save()

        return HttpResponseRedirect("/stock-analyzer/auth_home")


class SignOut(LogoutView):
    template_name = 'registration/logged_out.html'
    success_url_allowed_hosts = "/tweets/sign-in"


class SignIn(LoginView):
    success_url = "/tweets/auth_home"
    form_class = AuthenticationForm
    template_name = "tweets/signin.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect("/tweets/auth_home")


def home(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect("/tweets/sign-in")
    return render(request, 'tweets/home.html', context={
        'user' : user
    })
