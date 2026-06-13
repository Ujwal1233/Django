from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from account.models import LeaveRequest, Profile


def _get_or_create_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user, defaults={'role': 'staff'})
    return profile


def _is_admin(user):
    return _get_or_create_profile(user).role == 'admin'


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        requested_role = request.POST.get('role', 'staff')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, 'register.html')

        role = 'staff'
        if requested_role == 'admin':
            first_admin = not Profile.objects.filter(role='admin').exists()
            current_user_is_admin = request.user.is_authenticated and _is_admin(request.user)
            if first_admin or current_user_is_admin:
                role = 'admin'
            else:
                messages.error(request, 'Admin registration is not allowed from public signup.')
                return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, role=role)
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')
    return render(request, 'register.html')


def login(request):
    if request.user.is_authenticated:
        if _is_admin(request.user):
            return redirect('admin_dashboard')
        return redirect('hero')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            profile = _get_or_create_profile(user)
            if profile.role == 'admin':
                return redirect('admin_dashboard')
            return redirect('hero')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


@login_required
def hero(request):
    profile = _get_or_create_profile(request.user)
    if profile.role != 'staff':
        return redirect('admin_dashboard')

    leaves = LeaveRequest.objects.filter(user=request.user)
    context = {
        'pending_count': leaves.filter(status='pending').count(),
        'approved_count': leaves.filter(status='approved').count(),
        'rejected_count': leaves.filter(status='rejected').count(),
    }
    return render(request, 'Heropage.html', context)


@login_required
def admin_dashboard(request):
    if not _is_admin(request.user):
        messages.error(request, 'You are not authorized to access admin dashboard.')
        return redirect('hero')

    context = {
        'staff_count': Profile.objects.filter(role='staff').count(),
        'pending_requests': LeaveRequest.objects.filter(status='pending').count(),
        'total_requests': LeaveRequest.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def add_staff(request):
    if not _is_admin(request.user):
        messages.error(request, 'You are not authorized to add staff.')
        return redirect('hero')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'add_staff.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, 'add_staff.html')

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, role='staff')
        messages.success(request, 'Staff account created successfully.')
        return redirect('staff_list')

    return render(request, 'add_staff.html')


@login_required
def staff_list(request):
    if not _is_admin(request.user):
        messages.error(request, 'You are not authorized to view staff list.')
        return redirect('hero')

    staff_profiles = Profile.objects.filter(role='staff').select_related('user')
    return render(request, 'staff_list.html', {'staff_profiles': staff_profiles})


@login_required
def apply_leave(request):
    if _is_admin(request.user):
        messages.error(request, 'Admins cannot apply leave from staff portal.')
        return redirect('admin_dashboard')

    if request.method == 'POST':
        leave_type = request.POST.get('leave_type', '').strip()
        start_date = request.POST.get('start_date', '').strip()
        end_date = request.POST.get('end_date', '').strip()
        reason = request.POST.get('reason', '').strip()

        if not all([leave_type, start_date, end_date, reason]):
            messages.error(request, 'All fields are required.')
            return render(request, 'apply_leave.html')

        try:
            LeaveRequest.objects.create(
                user=request.user,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
            )
            messages.success(request, 'Leave request submitted successfully.')
            return redirect('my_leaves')
        except Exception as exc:
            messages.error(request, f'Unable to submit leave request: {exc}')

    return render(request, 'apply_leave.html')


@login_required
def my_leaves(request):
    if _is_admin(request.user):
        return redirect('all_leave_requests')

    leaves = LeaveRequest.objects.filter(user=request.user)
    return render(request, 'my_leaves.html', {'leaves': leaves})


@login_required
def all_leave_requests(request):
    if not _is_admin(request.user):
        messages.error(request, 'You are not authorized to view all leave requests.')
        return redirect('hero')

    leaves = LeaveRequest.objects.select_related('user').all()
    return render(request, 'all_leave_requests.html', {'leaves': leaves})


@login_required
def update_leave_status(request, leave_id, status):
    if not _is_admin(request.user):
        messages.error(request, 'You are not authorized to update leave status.')
        return redirect('hero')

    if status not in ['approved', 'rejected']:
        messages.error(request, 'Invalid leave status action.')
        return redirect('all_leave_requests')

    if request.method == 'POST':
        try:
            leave = LeaveRequest.objects.get(id=leave_id)
            if leave.status == 'pending':
                leave.status = status
                leave.admin_comment = request.POST.get('admin_comment', '').strip()
                leave.save()
                messages.success(request, f'Leave request {status} successfully.')
            else:
                messages.error(request, 'Only pending requests can be updated.')
        except LeaveRequest.DoesNotExist:
            messages.error(request, 'Leave request not found.')

    return redirect('all_leave_requests')


def logout_view(request):
    logout(request)
    return redirect('home')