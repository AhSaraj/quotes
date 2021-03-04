from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if(len(post_data['first_name']) < 3):
            errors['first_name'] = "first_name must be at least 4 characters"
        
        if(len(post_data['last_name']) < 3):
            errors['first_name'] = "first_name must be at least 4 characters"
            
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):            
            errors['email'] = "Invalid email address!"
        
        user = User.objects.filter(email=post_data['email'])
        if user:
            errors['email'] = "Email already used!"
        
        if (len(post_data['password']) < 5):
            errors['password'] = "Password must be at least 5 chars"
        if (post_data['confirm'] != post_data['password']):
            errors['password'] = "Passwords must match"

        return errors 
    
    def update_validator (self, post_data):
        errors = {}
        if(len(post_data['first_name']) < 3):
            errors['first_name'] = "first_name must be at least 4 characters"
        
        if(len(post_data['last_name']) < 3):
            errors['first_name'] = "first_name must be at least 4 characters"
            
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):            
            errors['email'] = "Invalid email address!"
        
        user = User.objects.filter(email=post_data['email'])
        if user:
            errors['email'] = "Email already used!"
            
        return errors
    
    
class QuoteManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if (len(post_data['author']) < 3):
            errors['author'] = "Must be min 3 char or more"
        
        if (len(post_data['quote']) < 10):
            errors['quote'] = "Quote must be min 10 char or more"
        return errors
        
        

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Quote(models.Model):
    author = models.CharField(max_length=100)
    quote = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="quote_uploaded", on_delete = models.CASCADE)
    liked_quote = models.ManyToManyField(User, related_name="liked_quote")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()