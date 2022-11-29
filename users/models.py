from django.contrib.auth.models import AbstractUser
from django.db import models


class Location (models.Model):
    name = models.CharField(max_length=150)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lng = models.DecimalField(max_digits=8, decimal_places=6)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


# class User(models.Model):
#     STATUS = [
#         ("member", "Участник"),
#         ("moderator", "Модератор"),
#         ("admin", "Админ")
#     ]
#
#     first_name = models.CharField(max_length=100, null=True, verbose_name='Имя')
#     last_name = models.CharField(max_length=200, null=True, verbose_name='Фамилия')
#     username = models.CharField(max_length=200, verbose_name='Логин', unique=True)
#     password = models.CharField(max_length=200, verbose_name='Пароль')
#     role = models.CharField(max_length=10, choices=STATUS, default="member")
#     age = models.PositiveIntegerField()
#     location = models.ManyToManyField(Location)
#
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#
#     def __str__(self):
#         return self.username


class User(AbstractUser):
    STATUS = [
                ("member", "Участник"),
                ("moderator", "Модератор"),
                ("admin", "Админ")
            ]

    role = models.CharField(max_length=10, choices=STATUS, default="member")
    age = models.PositiveIntegerField()
    location = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=200, null=True, verbose_name='Фамилия')
    username = models.CharField(max_length=200, verbose_name='Логин', unique=True)
    password = models.CharField(max_length=200, verbose_name='Пароль')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
