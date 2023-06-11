from django.db import models
import string
import random
from django.contrib.auth.models import AbstractUser, UserManager , AbstractBaseUser , BaseUserManager
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.contrib.auth.models import Group, Permission

from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
# from django.utils.text import slugify
from django.utils import timezone
from .choices import Choices
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible

@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename('images/products')
value_choices = Choices()

# https://fabric.inc/blog/ecommerce-database-design-example/
# https://testdriven.io/blog/django-custom-user-model/
# https://medium.com/djangotube/django-roles-groups-and-permissions-introduction-a54d1070544
# https://pdipesh.medium.com/django-rest-framework-permissions-example-8ed9809c432d
# https://medium.com/djangotube/django-roles-groups-and-permissions-introduction-a54d1070544


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None,user_type = "RGU",**extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.user_type=user_type
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_active", True)

        extra_fields.setdefault('user_type', 'SEL')  # Set user_type to "SEL"
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):

    # username = None
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    user_type = models.CharField(max_length=10, choices=value_choices.USER_TYPES,default="RGU")
    
    objects=CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    class Meta:
        managed = True
        db_table = 'users'

class TimestampedModel(models.Model):
    created_on = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='created_%(class)ss')
    updated_on = models.DateTimeField(default=now)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='updated_%(class)ss')

    class Meta:
        abstract = True

class Product(TimestampedModel):
    name = models.CharField(max_length=256)
    # sku =models.CharField(max_length=256,unique=True)
    category= models.ForeignKey("Category",models.DO_NOTHING)
    price = models.IntegerField(default=0)
    color =models.CharField(max_length=256)
    description =models.CharField(max_length=256)
    image =models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    quantity=models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta: 
        # permissions = [
        #     ("can_manage_product", "Can manage product"),  # Custom permission
        # ]
        managed = True
        db_table = 'products'


class Category(TimestampedModel):
    name = models.CharField(max_length=256)
    description =models.CharField(max_length=256)

    def __str__(self):
        return self.name
    
    class Meta: 
        managed = True
        db_table = 'product_categories'

class Inventory(TimestampedModel):
    quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.quantity)
    
    class Meta: 
        managed = True
        db_table = 'product_inventories'

class Discount(TimestampedModel):
    name = models.CharField(max_length=256)
    description =models.CharField(max_length=256)
    disconuted_percetage=models.IntegerField(default=0)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta: 
        managed = True
        db_table = 'product_discounts'

class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Passport(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    issue_date = models.DateField()

    def __str__(self):
        return self.number

# class Product(models.Model):
#     seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     # Add other fields for your product model

#     def __str__(self):
#         return self.name

#     class Meta:
#         permissions = [
#             ('can_manage_product', 'Can manage product'),
#         ]
