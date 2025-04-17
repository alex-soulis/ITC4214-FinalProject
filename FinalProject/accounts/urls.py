from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/',       views.register,           name='register'),
    path('login/',          views.user_login,         name='login'),
    path('logout/',         views.user_logout,        name='logout'),
    path('forgot-password/',views.forgot_password,    name='forgot_password'),
    path('dashboard/',      views.dashboard,          name='dashboard'),
    path('settings/',       views.profile,            name='profile'),

    # Employee management (Owner only)
    path('employees/',              views.manage_employees, name='manage_employees'),
    path('employees/add/',          views.add_employee,     name='add_employee'),
    path('employees/<int:employee_id>/edit/',   views.edit_employee,   name='edit_employee'),
    path('employees/<int:employee_id>/delete/', views.delete_employee, name='delete_employee'),
]
