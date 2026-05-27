import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fakeproject.settings')
django.setup()
from myapp.models import Employee
from faker import Faker
f=Faker('en_IN')
def populate(n):
    for i in range(n):
        fname=f.name()
        fdob=f.date_of_birth()
        fjob=f.job()
        fplace=f.city()
        femail=f.email()
        s=Employee.objects.get_or_create(name=fname, dob=fdob, job=fjob, place=fplace, email=femail)
populate(20)