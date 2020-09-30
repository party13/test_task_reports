from django.urls import path
from .views import *


urlpatterns = [
    path('login/', MyLogin.as_view(), name='login_url'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('password-change/', MyChangePassword.as_view(), name='password_change'),
    path('registration/<str:link>/', registration, name='password_reset')
]
