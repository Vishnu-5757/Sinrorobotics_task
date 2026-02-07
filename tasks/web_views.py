from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, Task
from django.contrib.auth import logout
from .forms import UserManagementForm,TaskForm


def is_superadmin(user):
    return user.is_authenticated and user.is_superadmin()

def is_admin_or_higher(user):
    return user.is_authenticated and (user.is_superadmin() or user.is_admin())



@login_required
def logout_view(request):
    """Custom logout to handle GET requests from links."""
    logout(request)
    return redirect('login')



@login_required
def dashboard(request):

    if request.user.is_superadmin():
        managed_users = User.objects.all()
        tasks = Task.objects.all()
    elif request.user.role == 'admin':
        managed_users = User.objects.filter(manager=request.user)
        tasks = Task.objects.filter(assigned_to__in=managed_users)
    else:
       
        managed_users = None  
        tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, 'admin/dashboard.html', {
        'tasks': tasks,
        'managed_users': managed_users,
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(status='completed').count(),
        'pending_tasks': tasks.filter(status='pending').count(),
    })



@login_required
@user_passes_test(is_superadmin)
def manage_users(request):
    """SuperAdmin only: Manage users and admins."""
    users = User.objects.all()
    # Remove the part entirely
    admins = User.objects.filter(role=User.ROLE_ADMIN) 
    return render(request, 'admin/manage_users.html', {'users': users, 'admins': admins})




@login_required
@user_passes_test(is_admin_or_higher)
def task_detail(request, pk):
    """View task completion reports and worked hours[cite: 18, 28, 34, 47, 67]."""
    task = get_object_or_404(Task, pk=pk)
    
    # Restriction: Admin can only see their users' tasks [cite: 35]
    if not request.user.is_superadmin() and task.assigned_to.manager != request.user:
        return redirect('dashboard')

    return render(request, 'admin/task_detail.html', {'task': task})




@login_required
@user_passes_test(is_superadmin)
def user_create(request):
    if request.method == 'POST':
        form = UserManagementForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('manage_users')
    else:
        form = UserManagementForm()
    return render(request, 'admin/user_form.html', {'form': form, 'title': 'Create User'})    



@login_required
@user_passes_test(is_superadmin)
def user_update(request, pk):
    user_to_edit = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        # instance=user_to_edit tells Django to update this specific user
        form = UserManagementForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            user = form.save(commit=False)
            # Only update password if a new one was provided
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('manage_users')
    else:
        form = UserManagementForm(instance=user_to_edit)
    
    return render(request, 'admin/user_form.html', {
        'form': form, 
        'title': f'Update User: {user_to_edit.username}'
    })




@login_required
@user_passes_test(is_superadmin)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user: # Prevent self-deletion
        user.delete()
    return redirect('manage_users')



@login_required
def manage_tasks(request):
    if request.user.is_superadmin():
        tasks = Task.objects.all().order_by('-created_at')
    elif request.user.role == 'admin':
        tasks = Task.objects.filter(assigned_to__manager=request.user).order_by('-created_at')
    else:
       
        tasks = Task.objects.filter(assigned_to=request.user).order_by('-created_at')
    
    return render(request, 'admin/manage_tasks.html', {'tasks': tasks})

@login_required
def task_upsert(request, pk=None):
    task = get_object_or_404(Task, pk=pk) if pk else None
    if task and request.user.role == 'user' and task.assigned_to != request.user:
        return redirect('manage_tasks')
    if not task and request.user.role == 'user':
        return redirect('manage_tasks')
    if request.method == 'POST':
       
        form = TaskForm(request.POST, instance=task, user=request.user)
        
        if form.is_valid():
            
            task_instance = form.save(commit=False)
            
            
            if request.user.role == 'user' and task:
                task_instance.title = task.title
                task_instance.assigned_to = task.assigned_to
                task_instance.description = task.description
                task_instance.due_date = task.due_date
            
            task_instance.save()
            return redirect('manage_tasks')
    else:
       
        form = TaskForm(instance=task, user=request.user)

        if request.user.role == 'user':
            for field_name in ['title', 'assigned_to', 'description', 'due_date']:
                if field_name in form.fields:
                    form.fields[field_name].disabled = True
    

    context_title = "Update Progress" if request.user.role == 'user' else ("Edit Task" if task else "Create Task")
    
    return render(request, 'admin/task_form.html', {
        'form': form,
        'task': task,
        'title': context_title
    })


@login_required
@user_passes_test(is_admin_or_higher) 
def task_reports(request):
    if request.user.is_superadmin():
        reports = Task.objects.filter(status=Task.STATUS_COMPLETED)
    else:
        reports = Task.objects.filter(
            status=Task.STATUS_COMPLETED, 
            assigned_to__manager=request.user
        )
    reports = reports.order_by('-created_at')
    return render(request, 'admin/task_reports.html', {
        'reports': reports
    })

@login_required
@user_passes_test(is_admin_or_higher)
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if not request.user.is_superadmin() and task.assigned_to.manager != request.user:
        return redirect('manage_tasks')
        
    task.delete()
    return redirect('manage_tasks')
