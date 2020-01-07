from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Логин', max_length=30, unique=True)
    email = models.EmailField('Электронная почта')
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    rating = models.IntegerField(default=0)
    ROCK = 'RK'
    RAP = 'RP'
    POP = 'PP'
    COUNTRY = 'CR'
    CLASSICAL = 'CL'
    HOUSE = 'HS'
    HATED_MUS_GENRE_CHOICES = (
        (ROCK, 'Рок'),
        (RAP, 'Рэп'),
        (POP, 'Поп'),
        (COUNTRY, 'Кантри'),
        (CLASSICAL, 'Классическая'),
        (HOUSE, 'Хаус'),
    )
    hated_mus_genre = models.CharField('Нелюбимый музыкальный жанр', max_length=2, choices=HATED_MUS_GENRE_CHOICES)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
