from django.urls import path
from . import views
from .views import *

app_name = 'account'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user_list/', user_list, name='user_list'),
    path('<int:user_id>/', profile, name='profile'),
    path('user_list/<int:user_id>/', create_staff, name='create_staff')
]
