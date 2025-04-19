# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.contrib.auth.models import Group
from django.contrib import messages
from cart.models import Order
from accounts.decorators import owner_or_employee_required, owner_required
from .forms import UserForm, UserProfileForm
from .models import UserProfile

User = get_user_model()

def register(request):
    error = None
    username = ""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        repeat   = request.POST.get('repeat-password', '')

        # Basic validation
        if not username or not password or not repeat:
            error = "All fields are required."
        elif password != repeat:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "That username is already taken."
        else:
            # Create the user
            User.objects.create_user(username=username, password=password)
            return redirect('accounts:login')

    return render(request, 'accounts/register.html', {
        'error': error,
        'username': username,
    })

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('shop:index')
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
    emp_group = Group.objects.get(name="Employee")
    employees = emp_group.user_set.all()   # every User in that group
    return render(request, 'accounts/employee_list.html', {
        'employees': employees
    })

@login_required
@owner_required
def add_employee(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # 1) save the built‑in User fields from the extra POST data:
            user.first_name = request.POST.get('first_name', '')
            user.last_name  = request.POST.get('last_name', '')
            user.email      = request.POST.get('email', '')
            user.save()

            # 2) save your UserProfile fields:
            profile = UserProfile.objects.create(
                user=user,
                phone_number=request.POST.get('phone_number', ''),
                # if you have an address or photo field, grab those too:
                # address=request.POST.get('address', ''),
                profile_photo=request.FILES.get('profile_photo'),
            )

            # 3) put them in the Employee group
            emp_group = Group.objects.get(name="Employee")
            user.groups.add(emp_group)

            messages.success(request, "Employee added successfully.")
            return redirect('accounts:manage_employees')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/add_employee.html', {
        'form': form
    })


@login_required
@owner_required
def edit_employee(request, employee_id):
    # grab the User
    employee = get_object_or_404(User, id=employee_id, groups__name='Employee')
    # grab or create the profile row
    profile, created = UserProfile.objects.get_or_create(user=employee)

    if request.method == "POST":
        user_form    = UserForm(request.POST,            instance=employee)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()       # writes first_name, last_name, email
            profile_form.save()    # writes phone_number, address
            messages.success(request, "Employee updated successfully.")
            return redirect('accounts:manage_employees')
    else:
        user_form    = UserForm(instance=employee)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'accounts/edit_employee.html', {
        'user_form':    user_form,
        'profile_form': profile_form,
        'employee':     employee,
    })

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
