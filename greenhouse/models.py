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
    staff_number = models.IntegerField(null=True,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    prof_photo = CloudinaryField('image', default='https://res.cloudinary.com/mwikali/image/upload/v1695192612/icons8-user-90_pt1zqi.png')
    phone_number = models.CharField(max_length=10, default='0701010101')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    groups = models.ManyToManyField('auth.Group',verbose_name='groups',blank=True,related_name='custom_users_groups')
    user_permissions = models.ManyToManyField('auth.Permission',verbose_name='user permissions',blank=True,related_name='custom_users_permissions')

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'greenhouse_user'
        # Add verbose name
        verbose_name = 'Staff Member'
    

class Production(models.Model):

    GREENHOUSE_NUMBERS = [
        ('1', 'GH 1'),
        ('2', 'GH 2'),
        ('3', 'GH 3'),
        ('4', 'GH 4'),
        ('5', 'GH 5'),
        ('6', 'GH 6'),
        ('7', 'GH 7'),
        ('8', 'GH 8'),
        ('9', 'GH 9'),
        ('10', 'GH 10'),
        ('11', 'GH 11'),
        ('12', 'GH 12'),
        ('13', 'GH 13'),
        ('14', 'GH 14'),
        ('15', 'GH 15'),
        ('16', 'GH 16'),
        ('17', 'GH 17'),
        ('18', 'GH 18'),
        ('19', 'GH 19'),
        ('20', 'GH 20'),
        ('21', 'GH 21'),
        ('22', 'GH 22'),
        ('23', 'GH 23'),
        ('24', 'GH 24'),
        ('25', 'GH 25'),
        ('26', 'GH 26'),
        ('27', 'GH 27'),
        ('28', 'GH 28'),
        ('29', 'GH 29'),
        ('30', 'GH 30'),
        ('31', 'GH 31'),
        ('32', 'GH 32'),
        ('33', 'GH 33'),
        ('34', 'GH 34'),
        ('35', 'GH 35'),
        ('36', 'GH 36'),
        ('37', 'GH 37'),
        ('38', 'GH 38'),
        ('39', 'GH 39'),
        ('40', 'GH 40'),
        ('41', 'GH 41'),
        ('42', 'GH 42'),
        ('43', 'GH 43'),
        ('44', 'GH 44'),
        ('45', 'GH 45'),
        ('46', 'GH 46'),
        ('47', 'GH 47'),
        ('48', 'GH 48'),
        ('49', 'GH 49'),
        ('50', 'GH 50'),
        ('51', 'GH 51'),
        ('52', 'GH 52'),
        ('53', 'GH 53'),
        ('54', 'GH 54'),
        ('55', 'GH 55'),
        ('56', 'GH 56'),
        ('57', 'GH 57'),
        ('58', 'GH 58'),
        ('59', 'GH 59'),
        ('60', 'GH 60'),
        ('61', 'GH 61'),
        ('62', 'GH 62')
    ]
    VARIETIES_CHOICES = [
        ('Athena', 'Athena'),
        ('Belle Rose', 'Belle Rose'),
        ('Confidential', 'Confidential'),
        ('Espana', 'Espana'),
        ('Esperance', 'Esperance'),
        ('Ever Red', 'Ever Red'),
        ('Fire Expressions', 'Fire Expressions'),
        ('Fuschiana', 'Fuschiana'),
        ('Golden Finch', 'Golden Finch'),
        ('Good times', 'Good times'),
        ('Jumilia', 'Jumilia'),
        ('Madam Cerise', 'Madam Cerise'),
        ('Madam Pink', 'Madam Pink'),
        ('Madam Red', 'Madam Red'),
        ('Magic Avalanche+', 'Magic Avalanche+'),
        ('Mandala', 'Mandala'),
        ('Miss Mardi', 'Miss Mardi'),
        ('Moonwalk', 'Moonwalk'),
        ('New Orleans', 'New Orleans'),
        ('Novavita', 'Novavita'),
        ('Opala', 'Opala'),
        ('Revival', 'Revival'),
        ('Tacazzi+', 'Tacazzi+'),
        ('Tara', 'Tara'),
        ('Wham', 'Wham'),
        ('Yellowing', 'Yellowing'),
    ]

    production_date = models.DateField(auto_now=True)
    greenhouse_number = models.CharField(max_length=50, choices=GREENHOUSE_NUMBERS, default='GH 1')
    varieties = models.CharField(max_length=50, choices=VARIETIES_CHOICES,default='Athena') 
    total_number = models.IntegerField(default=0)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)


    def __str__(self):
        return f"Production for {self.production_date}"

class RejectedData(models.Model):

    GREENHOUSE_NUMBERS = [
        ('1', 'GH 1'),
        ('2', 'GH 2'),
        ('3', 'GH 3'),
        ('4', 'GH 4'),
        ('5', 'GH 5'),
        ('6', 'GH 6'),
        ('7', 'GH 7'),
        ('8', 'GH 8'),
        ('9', 'GH 9'),
        ('10', 'GH 10'),
        ('11', 'GH 11'),
        ('12', 'GH 12'),
        ('13', 'GH 13'),
        ('14', 'GH 14'),
        ('15', 'GH 15'),
        ('16', 'GH 16'),
        ('17', 'GH 17'),
        ('18', 'GH 18'),
        ('19', 'GH 19'),
        ('20', 'GH 20'),
        ('21', 'GH 21'),
        ('22', 'GH 22'),
        ('23', 'GH 23'),
        ('24', 'GH 24'),
        ('25', 'GH 25'),
        ('26', 'GH 26'),
        ('27', 'GH 27'),
        ('28', 'GH 28'),
        ('29', 'GH 29'),
        ('30', 'GH 30'),
        ('31', 'GH 31'),
        ('32', 'GH 32'),
        ('33', 'GH 33'),
        ('34', 'GH 34'),
        ('35', 'GH 35'),
        ('36', 'GH 36'),
        ('37', 'GH 37'),
        ('38', 'GH 38'),
        ('39', 'GH 39'),
        ('40', 'GH 40'),
        ('41', 'GH 41'),
        ('42', 'GH 42'),
        ('43', 'GH 43'),
        ('44', 'GH 44'),
        ('45', 'GH 45'),
        ('46', 'GH 46'),
        ('47', 'GH 47'),
        ('48', 'GH 48'),
        ('49', 'GH 49'),
        ('50', 'GH 50'),
        ('51', 'GH 51'),
        ('52', 'GH 52'),
        ('53', 'GH 53'),
        ('54', 'GH 54'),
        ('55', 'GH 55'),
        ('56', 'GH 56'),
        ('57', 'GH 57'),
        ('58', 'GH 58'),
        ('59', 'GH 59'),
        ('60', 'GH 60'),
        ('61', 'GH 61'),
        ('62', 'GH 62')
    ]
    VARIETIES_CHOICES = [
        ('Athena', 'Athena'),
        ('Belle Rose', 'Belle Rose'),
        ('Confidential', 'Confidential'),
        ('Espana', 'Espana'),
        ('Esperance', 'Esperance'),
        ('Ever Red', 'Ever Red'),
        ('Fire Expressions', 'Fire Expressions'),
        ('Fuschiana', 'Fuschiana'),
        ('Golden Finch', 'Golden Finch'),
        ('Good times', 'Good times'),
        ('Jumilia', 'Jumilia'),
        ('Madam Cerise', 'Madam Cerise'),
        ('Madam Pink', 'Madam Pink'),
        ('Madam Red', 'Madam Red'),
        ('Magic Avalanche+', 'Magic Avalanche+'),
        ('Mandala', 'Mandala'),
        ('Miss Mardi', 'Miss Mardi'),
        ('Moonwalk', 'Moonwalk'),
        ('New Orleans', 'New Orleans'),
        ('Novavita', 'Novavita'),
        ('Opala', 'Opala'),
        ('Revival', 'Revival'),
        ('Tacazzi+', 'Tacazzi+'),
        ('Tara', 'Tara'),
        ('Wham', 'Wham'),
        ('Yellowing', 'Yellowing'),
    ]
    REJECTION_REASONS = [
        ('BENT STEMS', 'BENT STEMS'),
        ('GOOSE NECKS', 'GOOSE NECKS'),
        ('BULL HEADS', 'BULL HEADS'),
        ('OFF COLOUR', 'OFF COLOUR'),
        ('WEAK STEMS', 'WEAK STEMS'),
        ('YELLOWING', 'YELLOWING'),
        ('APHIDS', 'APHIDS'),
        ('CATERPILLARS', 'CATERPILLARS'),
        ('MITES', 'MITES'),
        ('THRIPS', 'THRIPS'),
        ('POWDERY MILDEW', 'POWDERY MILDEW'),
        ('DOWNEY', 'DOWNEY'),
        ('BOTRYTIS', 'BOTRYTIS'),
        ('BROKEN STEMS', 'BROKEN STEMS'),
        ('Bruises & Mechanical damages', 'Bruises & Mechanical damages'),
        ('CHEMICAL SCORCHES', 'CHEMICAL SCORCHES'),
        ('CHEMICAL RESIDUE', 'CHEMICAL RESIDUE'),
        ('MUTATION', 'MUTATION'),
        ('TOO OPEN', 'TOO OPEN'),
        ('UNDER SIZE', 'UNDER SIZE'),
        ('ROTTEN', 'ROTTEN'),
        ('SMALL HEADS', 'SMALL HEADS'),
    ]


    rejection_date = models.DateField(auto_now_add=True)
    greenhouse_number = models.CharField(max_length=50, choices=GREENHOUSE_NUMBERS, default ='GH 1')
    varieties = models.CharField(max_length=50, choices=VARIETIES_CHOICES,default='Athena') 
    rejected_number = models.IntegerField(default=0)
    rejection_reason = models.CharField(max_length=50,choices=REJECTION_REASONS, default='Bent Stems')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'Rejection Data for {self.rejection_date}'



