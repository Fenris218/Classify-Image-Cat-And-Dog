print(">>> classifier.urls LOADED <<<")
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"), 
    path("login/", views.login_view, name="login"),
    path("upload/", views.upload_view, name="upload"),
    path("result/<int:job_id>/", views.result_view, name="result"),
    path("job-status/<int:job_id>/", views.job_status_view, name="job_status"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("history/", views.history_view, name="history")
    
]

