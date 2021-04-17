from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView

from tweets.forms import SearchForm

aws_access_key_id="ASIARXUC647CZM3TEXGY"
aws_secret_access_key="brHf49eXOOyZ7TErvyN0fr4Psf/7Y068LAKuzKoq"
aws_session_token="FwoGZXIvYXdzEBwaDNyySWVFnd9Kb/a21CLCAZV9qfmLSPeRSInJiBeDdcjD1v24NTIxg3vh0JukqlrFjpO8CU5sXcUjpXuQ1/5bxdAGDtSOozyzdEkdj8xsvMFri+o3WMAr6fR3TRBTK1GZFkxkRB1fwGV9UGaHfvtRJgt1D+754Ao9DP+OXoW0KfjQHQ1T8d3imRLvhLydMKnQoQLKZnTpzGrNvk/wH9X8OTG9igTDnyqKoP+s00DDKFpntFvQaNiUnnVeyLnf5VqLg9JcuA+CblYUrsQC9JY6zvLzKK/ClIIGMi3CKFtWNmwRwSvZU4lHpbTS2rfEo5L+jxbHzpujJCHSz0/SmMU1YMLKQ2xSZUs="


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/tweets/auth_home")
    else:       # Unregistered User
        return HttpResponseRedirect("/tweets/sign-up")


class SignUp(FormView):
    success_url = "/tweets/auth_home/"
    form_class = UserCreationForm
    template_name = "tweets/signup.html/"

    def form_valid(self, form):
        form.save()
        user = User.objects.get(username=form.data.get('username'))
        login(self.request, user)
        form.save()

        return HttpResponseRedirect("/tweets/auth_home")


class SignOut(LogoutView):
    template_name = 'registration/logged_out.html'
    success_url = "/tweets/sign-in"

class AboutUs(FormView):
    success_url = "/tweets/auth_home/"
    form_class = AuthenticationForm
    template_name = "tweets/about-us.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect("/tweets/auth_home/")


class SignIn(LoginView):
    success_url = "/tweets/auth_home/"
    form_class = AuthenticationForm
    template_name = "tweets/signin.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect("/tweets/auth_home/")


def home(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect("/tweets/sign-in/")
    return render(request, 'tweets/home.html', context={
        'user': user,
        'form': SearchForm()
    })


class Search(FormView):
    form_class = SearchForm
    template_name = 'tweets/home.html'
    success_url = "display/"


def display(request):
    return render(request, 'tweets/search-results.html')
