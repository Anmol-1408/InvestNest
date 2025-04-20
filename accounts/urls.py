from django.urls import path
from . import views

# app_name = 'accounts'  # Optional: helps when using namespaced URLs

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile_setup/', views.profile_setup, name='profile_setup'),
]


# 🧠 Why add app_name = 'accounts'?
# This allows you to reference URLs in templates and views like:

# html
# Copy
# Edit
# {% url 'accounts:login' %}
# {% url 'accounts:profile' %}
# Or from code:

# python
# Copy
# Edit
# reverse('accounts:signup')
# This helps avoid name clashes if you have similar route names in other apps (e.g., admin, dashboard, users).


