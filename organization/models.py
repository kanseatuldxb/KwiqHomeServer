import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Employee(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # unique email false
    email = models.EmailField(max_length=255, unique=False,)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    user_type = models.CharField(max_length=100,choices=[
        ('CEO','CEO'),
        ('Manager','Manager'),
        ('LocalityManager','Locality Manager'),
        ('Caller','Caller'),
        ('Visitor','Visitor'),
        ('VisitorCaller','Visitor and Caller'),
    ], blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = None
    last_name = None
    name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    assigned_to = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='assigned_employees', null=True, blank=True)
    locality = models.CharField(max_length=100,
                                choices=[
                                    ('east','East'),
                                    ('west','West'),
                                    ('north','North'),
                                    ('south','South'),
                                    ('central','Central'),
                                ],
                                blank=True, null=True)
    def __str__(self):
        return f'{self.name} - {self.organization}'

    class Meta:
        # email and username should be unique together for each organization
        unique_together = ['email', 'organization']

