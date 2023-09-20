from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings

from cloudinary.models import CloudinaryField
from django.utils import timezone

# Create your models here.
# User class
class CustomUserManager(BaseUserManager):
    def create_user(self, email,password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(default=timezone.now)
    staff_number = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    groups = models.ManyToManyField('auth.Group',verbose_name='groups',blank=True,related_name='custom_users_groups')
    user_permissions = models.ManyToManyField('auth.Permission',verbose_name='user permissions',blank=True,related_name='custom_users_permissions')

    def __str__(self):
        return self.full_name

    
class Production(models.Model):
    production_date = models.DateField(auto_now_add=True)
    greenhouse_number = models.IntegerField()
    variety = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    rejected_flowers = models.IntegerField(null=True, blank=True)
    rejection_reason = models.CharField(max_length=100, blank=True, null=True)
    staff_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)    


    def __str__(self):
        return f"Production for {self.production_date}"

class Profile(models.Model):
    prof_photo = CloudinaryField('image')
    phone_number = models.CharField(max_length=10)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"Profile for {self.user}"

    def save_profile(self):
        self.save()

    def update_profile(self):
        self.save()

    @classmethod
    def get_profile_by_user(cls, user):
        profile = cls.objects.filter(user=user)
        return profile