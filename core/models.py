from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from .mailing import send_gmail
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def email_user(self, *args, **kwargs):
        """
        subject: first argument\n
        message: second argument
        """
        send_gmail(
            '{}'.format(args[0]), # Subject
            '{}'.format(args[1]), # Message
            self.email,
            )


    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField(unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = '-'.join(str(self.name).lower().split())
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class VoteItem(models.Model):
    name = models.CharField(max_length=50)
    # TODO: image = models.ImageField(upload_to=None)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Profile(models.Model):

    person = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=True)
    first_name = models.CharField("First Name", blank=True, max_length=20)
    last_name = models.CharField("Last Name", blank=True, max_length=20)
    votes = models.ManyToManyField(VoteItem)
    categories_voted = models.ManyToManyField(Category)

    def get_full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
        
    def __str__(self):
        return self.person.email

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()