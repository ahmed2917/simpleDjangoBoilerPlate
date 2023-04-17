from django.urls import path
from account_management.views import Signup, Signin

urlpatterns = [
    path('signup/', Signup.as_view(), name="signup"),
    path('signin/', Signin.as_view(), name="signin"),
]
