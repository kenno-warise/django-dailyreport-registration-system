from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    user_no = models.CharField(verbose_name="社員番号", max_length=4)

# Create your models here.
