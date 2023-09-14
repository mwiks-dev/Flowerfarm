from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User



# Create your models here.
class Production(models.Model):
    production_date = models.DateField(auto_now_add=True)
    greenhouse_number = models.IntegerField()
    variety = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    staff_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rejected_flowers = models.IntegerField(null=True, blank=True)
    rejection_reason = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Production for {self.production_date}"