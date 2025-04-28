from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
UserRole_CHOICES = (
    ('admin', 'Admin'),
    ('employee', 'Employee'),
    ('manager', 'Manager'),
)

class Usercustome(AbstractUser):
    phone_number  = models.CharField(max_length=10)
    user_role = models.CharField(max_length=10, choices=UserRole_CHOICES, default='employee') 
 
 
 
 