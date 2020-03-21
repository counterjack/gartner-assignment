from django.db import models
import enum

class UserGroups(enum.Enum):
    Manager = "Manager"
    Associate = "Associate"
    Client = "Client"

class TimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# class UserTimeMixin():