from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileForm
from cart.models import Order
from accounts.decorators import owner_or_employee_required
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('acconts:dashboard')
        else:
            error = "Invalid credentials"
            return render(request, 'acconts/login.html', {'error': error})
    return render(request, 'accounts/login.html')

@login_required
def dashboard(request):
    orders = Order.objects.filter(user = request.user)
    return render(request, 'accounts/dashboard.html', {'orders': orders})

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('acconts:dashboard')
    else:
        form = ProfileForm(instance = request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
@owner_or_employee_required("Owner")
def manage_employees(request):
    employees = User.objects.filter(groups__name = 'Employee')
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "delete":
            employee_id = request.POST.get("employee_id")
            if employee_id:
                employee = get_object_or_404(User, id = employee_id, groups__name = 'Employee')
                employee.delete()
                messages.success(request, "Employee deleted successfully")
                return redirect ("accounts: manage_employees")
    
    context = {
        'employees' : employees
    }

    return render(request, 'accounts/manage_employees.html', context)