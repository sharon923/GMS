from django.conf import settings
from django.urls import path
from . import views
from .public_user.views import UserProfile, UserHome
from .employ.views import EmployHome
from .common.views import LoginView, SignupView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordChangeDoneView


urlpatterns = [
    # Website page
    path('', views.index, name='home'),
    # Common routes
    path('login', LoginView.as_view(), name='login'),
    path('user_logout', LogoutView.as_view(), name='user_logout'),
    path('signup', SignupView.as_view(), name='signup'),
    # Employ home related routes
    path('emp_home', EmployHome.as_view(), name='emp_home'),
    # Public user routes
    path('home', UserHome.as_view(), name='user_home'),
    path('user_profile', UserProfile.as_view(), name='user_profile'),
    # To be optimized or removed routes
    path('price', views.price, name='price'),
    path('price_details', views.price_details, name='price_details'),
    path('subscribe', views.subscribe, name='subscribe'),

]