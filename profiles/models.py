






from datetime import datetime
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import UserManager
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=150, unique=True)    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin




GENDER=(
    ('0', 'Female'),
    ('1', 'Male'),
)

class Location(models.Model):
    name=models.CharField(max_length=100, default='Nairobi', blank=True)

    def __str__(self):
        return self.name
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='profiles/default.png', upload_to='profiles')
    about = models.TextField(default='', blank=True)
    fname = models.CharField(max_length=300)
    phone = models.CharField(max_length=13)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    location=models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER,
        default='0'
    )
    age=models.PositiveIntegerField(
        default=18,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(18),
        ]
    )
    
    services=models.CharField(max_length=200)
    is_paid=models.BooleanField(default=False)

    class Meta:
        ordering=['-created_on']

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username':self.user.username})


class Contact(models.Model):
    
    name = models.CharField(max_length=80, default='')
    email = models.EmailField(default='')
    mobile=models.CharField(max_length=15, default='')
    body = models.TextField(default='')
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()