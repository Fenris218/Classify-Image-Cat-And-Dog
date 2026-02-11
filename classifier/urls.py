print(">>> classifier.urls LOADED <<<")
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"), 
    path("login/", views.login_view, name="login"),
    path("upload/", views.upload_view, name="upload"),
    path("result/", views.result_view, name="result"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("history/", views.history_view, name="history")
    
]

