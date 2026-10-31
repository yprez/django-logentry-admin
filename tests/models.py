from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class Member(AbstractBaseUser):
    """A custom user model whose primary key is not called "id"."""

    member_number = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "name"


class Batch(models.Model):
    """A model with a text primary key, which admin URLs quote."""

    code = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.code
