from django.urls import path
from . import views

urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('signup/', views.user_signup, name='signup'),
	path('profile/', views.profile, name='profile'),
    path('profile_setup/', views.profile_setup, name='profile_setup'),

]
