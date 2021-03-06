from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date

from tweets.forms import SearchForm, TrendsFilterForm
from tweets.graphAnalysis.woied_helpers import get_trending, get_woeid
from tweets.forms import SearchForm
import datetime as datetime

from datetime import datetime, timedelta
from tweets.graphAnalysis.graphSentiment import generate_graph



def index(request):
    return HttpResponseRedirect("/tweets/auth_home")

"""
    Standard sign up view for creating new users
"""
class SignUp(FormView):
    success_url = "/tweets/auth_home/"
    form_class = UserCreationForm
    template_name = "tweets/signup.html/"

    '''overriding so we can login in the user'''
    def form_valid(self, form):
        form.save()
        user = User.objects.get(username=form.data.get('username'))
        login(self.request, user)
        form.save()

        return HttpResponseRedirect("/tweets/auth_home")


"""
Standard logout view for the site 
"""
class SignOut(LogoutView):
    template_name = 'registration/logged_out.html'
    success_url = "/tweets/sign-in"


class AboutUs(FormView):
    success_url = "/tweets/auth_home/"
    form_class = AuthenticationForm
    template_name = "tweets/about-us.html"


class ContactUs(FormView):
    success_url = "/tweets/auth_home/"
    form_class = AuthenticationForm
    template_name = "tweets/contact-us.html"


"""
Standard login view for the site 
"""
class SignIn(LoginView):
    success_url = "/tweets/auth_home/"
    form_class = AuthenticationForm
    template_name = "tweets/signin.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect("/tweets/auth_home/")


''' Method used for returning the search form '''
def home(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect("/tweets/sign-in/")
    return render(request, 'tweets/home.html', context={
        'user': user,
        'form': SearchForm(),
    })


"""
    takes in the search query and returns the graphs
"""
class Search(FormView):
    form_class = SearchForm
    template_name = 'tweets/home.html'
    success_url = "display/"

    def form_valid(self, form):
        search = form.cleaned_data['search']
        region = form.cleaned_data['region']
        end_date = date.today()
        result_type = form.cleaned_data['result_type']
        return HttpResponseRedirect(self.get_success_url() + str(search) + '/'+ str(region) + '/'
                                    + str(end_date) + '/' + str(result_type) + '/')


"""
    View used for filering the 'trends' page by location
"""
class FilterTrends(FormView):
    form_class = TrendsFilterForm
    template_name = "tweets/filter-trending.html"
    success_url = "display/"

    def form_valid(self, form):
        date = datetime.now().strftime('%Y-%m-%d')
        location = form.cleaned_data['location']
        return HttpResponseRedirect(self.get_success_url() + str(location)+'/'+str(date)+'/')


'''Displays graph based on search query.'''
def display(request, search=None, region=None, end_date=None, result_type=None):
    graph, overall_sentiment = generate_graph(search, region, result_type)  # helper function used for making graphs

    context = {'graph': graph,
               'search': search,
               'region': region,
               'end_date': end_date,
               'sentiment': overall_sentiment,
               'result_type': result_type}
    return render(request, 'tweets/search-results.html', context)


def display_trends(request, woeid=1, date=None):
    trends = get_trending(woeid=woeid)[0].get('trends')  # display trends based on a certain location, or default to 1
    page = request.GET.get('page', 1)                    # (worldwide trends)
    paginator = Paginator(trends, 10)

    # Pagination logic
    try:
        trends = paginator.page(page)
    except PageNotAnInteger:
        trends = paginator.page(1)
    except EmptyPage:
        trends = paginator.page(paginator.num_pages)

    return render(request, 'tweets/trending.html', context=dict(trends=trends, date=date))

