from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, CustomUserCreationForm

# Create your views here.

def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('profile')
		else:
			return render(request, 'login.html', {'error': 'Invalid username or password'})
	return render(request, 'accounts/login.html')

def user_logout(request):
	logout(request)
	return redirect('login')

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_setup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_setup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile_setup.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile  # Get the profile linked to the logged-in user
    return render(request, 'accounts/profile.html', {'profile': profile})
