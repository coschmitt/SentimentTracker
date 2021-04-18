from django.contrib import admin
from django.urls import path

from tweets import views

urlpatterns = [
    path("", views.index, name='home'),
    path("sign-up/", views.SignUp.as_view(), name="sign-up"),
    path("sign-in/", views.SignIn.as_view(), name="sign-in"),
    path("auth_home/", views.home, name="auth_home"),
    path("signout/", views.SignOut.as_view(), name='sign-out'),
    path('search/', views.Search.as_view(), name='search'),
    path('search/display/<search>/<region>/<end_date>/<result_type>/', views.display, name='display-results'),
    path("about-us/", views.AboutUs.as_view(), name="about-us"),
    path("contact-us/", views.ContactUs.as_view(), name="contact-us"),
    path('trending/', views.FilterTrends.as_view(), name='filter-trends'),
    path("trending/display/<woeid>/", views.display_trends, name="trending"),


]