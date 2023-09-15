from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField



# Create your models here.
class Production(models.Model):
    production_date = models.DateField(auto_now_add=True)
    greenhouse_number = models.IntegerField()
    variety = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    staff_member = models.OneToOneField(User, on_delete=models.SET_NULL , null=True)
    rejected_flowers = models.IntegerField(null=True, blank=True)
    rejection_reason = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Production for {self.production_date}"

class Profile(models.Model):
    prof_photo = CloudinaryField('image')
    phone_number = models.CharField(max_length=10)
    staff_number = models.IntegerField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"Profile for {self.staff_number}"

    def save_profile(self):
        self.save()

    def update_profile(self):
        self.save()

    @classmethod
    def get_profile_by_user(cls, user):
        profile = cls.objects.filter(user=user)
        return profile