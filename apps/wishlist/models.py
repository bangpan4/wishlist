from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = 'Name must contain at least 3 letters'
        if len(postData['username']) < 3:
            errors['username'] = 'Username must contain at least 3 letters'
        if len(postData['password']) < 8:
            errors['email_length'] = 'Password must contain at least 8 characters'
        if postData['password'] != postData['password_con']:
            errors['password'] = 'Password not match'
        try:
            User.objects.get(username=postData['username'])
            errors['username_exist'] = 'This username has been already registered'
        except:
            pass
        return errors;

    def wish_validator(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors['item'] = 'Item name must contain at least 3 letters'
        return errors;

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wishlist(models.Model):
    item = models.CharField(max_length=45)
    creator = models.ForeignKey(User, related_name = 'items')
    want = models.ManyToManyField(User,related_name = 'wants')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()