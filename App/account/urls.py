from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register, name='register'),
    path("log_in/", log_in, name='log_in'),
    path("log_out/", log_out, name='log_out'),
    path("dashboard/", dashboard, name="dashboard"),
    path("", dashboard, name="dashboard"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("forget/", forget_password, name="forget_pass"),
    path("reset_pass_validation/<uidb64>/<token>/", reset_pass_valided, name="reset_pass_valided"),
    path("reset_password/", resetpassword, name="resetpassword")

]