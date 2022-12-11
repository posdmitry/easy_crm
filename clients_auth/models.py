from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class CustomUser(AbstractUser):
    company = models.ForeignKey(Company, related_name='company', null=True, default=1, on_delete=models.PROTECT)
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
