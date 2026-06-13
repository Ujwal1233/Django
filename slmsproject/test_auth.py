import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','slmsproject.settings')
import django
django.setup()
from django.contrib.auth import get_user_model, authenticate
User = get_user_model()
exists = User.objects.filter(username='tempuser').exists()
print('exists', exists)
if not exists:
    User.objects.create_user('tempuser', password='TempPass123')
    print('created')
a = authenticate(username='tempuser', password='TempPass123')
print('auth_ok', a is not None, a)
