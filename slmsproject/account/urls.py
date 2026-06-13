from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('hero/', hero, name='hero'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('add_staff/', add_staff, name='add_staff'),
    path('staff_list/', staff_list, name='staff_list'),
    path('apply_leave/', apply_leave, name='apply_leave'),
    path('my_leaves/', my_leaves, name='my_leaves'),
    path('all_leave_requests/', all_leave_requests, name='all_leave_requests'),
    path('update_leave_status/<int:leave_id>/<str:status>/', update_leave_status, name='update_leave_status'),
    path('logout/', logout_view, name='logout'),
]