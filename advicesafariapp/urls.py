from django.urls import path
from . import views  # Import the views module from your app
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name="home"),
    path('index', views.index, name="index"),
    path('signin', views.signin, name="signin"),
    path('register/', views.register, name='register'),
    path('listyourproperty', views.listyourproperty, name="listyourproperty"),
    path('booking', views.booking, name="booking"),
    path('user_logout/',views.logout_view, name='user_logout'),
    path('forget_password/',views.forgot_password,name="forget_password"),
    path('password_reset_sent/<str:reset_id>/',views.password_reset_sent,name="password_reset_sent"),
    path('change_password/<str:reset_id>/',views.change_password,name="change_password"),

    # other URL patterns
]