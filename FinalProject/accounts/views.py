from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render (request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        uername = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    else:
        error = "Invalid username or password."
        return render(request, 'accounts/login.html', {'error': error})
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect ('index')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, intsance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def dashboard(request):
    recent_activity = []
    context = {
        'recent_activity' : recent_activity
    }
    return render(request, 'accounts/dashboard.html', context)


