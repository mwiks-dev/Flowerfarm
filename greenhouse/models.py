from django.db import models

# Create your models here.

class Production(models.Model):
    production_date = models.DateField()
    greenhouse_number = models.IntegerField()
    variety = models.CharField(max_length=50)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    staff_number = models.IntegerField()
    rejected_flowers = models.IntegerField(default=0)
    rejection_reason = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.greenhouse_number