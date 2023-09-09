from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


# Create your models here.

# User class
class User(AbstractUser):
    # Define the extra fields related to User here
    first_name = models.CharField(_('First Name of User'),null = True, max_length = 20)
    last_name = models.CharField(_('Last Name of User'),null = True, max_length = 20)
    email = models.EmailField(unique=True)
    staff_number = models.IntegerField(null=True)

    groups = models.ManyToManyField('auth.Group', verbose_name=_('groups'), blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', verbose_name=_('user permissions'), blank=True, related_name='custom_user_permissions')
                              
    #custom permissions related to User.
    class Meta:
        ordering = ['-staff_number']

        permissions = (
            ("can edit", "To provide edit form"),
            ("can download reports", "To provide download access")
            )

class Production(models.Model):
    production_date = models.DateField()
    greenhouse_number = models.IntegerField()
    variety = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    staff = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    rejected_flowers = models.IntegerField(null=True, blank=True)
    rejection_reason = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.greenhouse_number