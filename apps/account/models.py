from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserGender(models.TextChoices):
        male = 'male', 'آقا'
        female = 'female', 'خانم'

    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل')
    avatar = models.ImageField(upload_to='images/user_panel/user_photo', verbose_name='تصویر / آواتار', null=True,
                               blank=True)
    mobile = models.CharField(max_length=14, verbose_name='تلفن همراه', null=True, blank=True)
    address = models.TextField(verbose_name='آدرس', null=True, blank=True)
    birthdate = models.DateField(verbose_name='تاریخ تولد', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=UserGender.choices, verbose_name='جنسیت', null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True, verbose_name='نام کاربری')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        elif self.email:
            return self.email

        return self.username
