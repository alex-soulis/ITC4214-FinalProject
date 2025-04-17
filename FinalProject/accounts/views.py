# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.contrib.auth.models import Group
from django.contrib import messages
from cart.models import Order
from accounts.decorators import owner_or_employee_required, owner_required

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accounts:dashboard')
        messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:login')

def forgot_password(request):
    # stub—hook up Django’s PasswordResetForm + email backend as needed
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request,
                      use_https=request.is_secure(),
                      email_template_name='accounts/password_reset_email.html')
            messages.success(request, "Password reset instructions sent.")
            return redirect('accounts:login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'accounts/order-history.html', {'orders': orders})

@login_required
def profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:settings')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'accounts/settings.html', {'form': form})

@login_required
@owner_required
def manage_employees(request):
    employees = User.objects.filter(groups__name='Employee')
    return render(request, 'accounts/list_employees.html', {'employees': employees})

@login_required
@owner_required
def add_employee(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            employee_group, _ = Group.objects.get_or_create(name='Employee')
            user.groups.add(employee_group)
            messages.success(request, "Employee created successfully.")
            return redirect('accounts:manage_employees')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/add_employee.html', {'form': form})

@login_required
@owner_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(User, id=employee_id, groups__name='Employee')
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect('accounts:manage_employees')
    else:
        form = UserChangeForm(instance=employee)
    return render(request, 'accounts/edit_employee.html', {'form': form, 'employee': employee})

@login_required
@owner_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(User, id=employee_id, groups__name='Employee')
    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee deleted successfully.")
        return redirect('accounts:manage_employees')
    # Optional: render a confirmation template
    return render(request, 'accounts/employee_list.html', {'employee': employee})
