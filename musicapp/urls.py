from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.index , name = 'index'),
    path('account/login/' , views.login_user , name = 'login'),
    path('account/logout/' , views.logout_user , name = 'logout'),
    path('account/signup/' , views.signup_user , name = 'signup'),
]