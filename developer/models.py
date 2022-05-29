from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.conf import settings
from authority.models import AlgoDetails

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Email is required")

        user=self.model(
            email = self.normalize_email(email),
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username = username,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user




class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=60,unique=True)
    username = models.CharField(max_length=30)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True



class ratingAlgs(models.Model):
    Rateduser = models.IntegerField(default=0)
    
    algs = models.ForeignKey(AlgoDetails,on_delete=models.CASCADE)
    ratings = models.IntegerField(default=0)
    review = models.CharField(max_length=200)
