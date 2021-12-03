from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, fname, lname, dob, password=None):
        """Creates a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, fname=fname, lname=lname, dob=dob)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, fname, lname, dob, password):
        """Creates a new superuser with given details"""
        user = self.create_user(email, fname, lname, dob, password)
        user.is_superuser = True

        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """DataBase models for users in the systems"""
    email = models.EmailField(max_length=255, unique=True)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    dob = models.DateField()
    profile_pic = models.ImageField(upload_to='profile_pic/%Y/%m/%d/', default='images/default_profile_pic.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    otp = models.IntegerField(blank=True, null=True)
    friends = models.ManyToManyField("User", blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname', 'dob']

    def get_full_name(self):
        """Retrive full name of user"""
        return self.fname + " " + self.lname

    def get_short_name(self):
        """Retrive short name of user"""
        return self.fname

    def get_email(self):
        """Retrieves email of user"""
        return self.email

    def get_dob(self):
        """Retrieves dob of user"""
        return self.dob

    def __str__(self):
        """Return string representation of our user"""
        return self.email

    def get_username(self):
        """Returns username by dividing email"""
        return self.email.split('@')[0]

class UserRelationShip(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user_chat', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_chat')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns representation of relation between users"""
        return f"{self.from_user.get_full_name()} -> {self.to_user.get_full_name()}"
