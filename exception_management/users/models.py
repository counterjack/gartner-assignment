from django.db import models
from core.models import TimeMixin
# Create your models here.
from django.contrib.auth.models import User
from django_fsm import FSMField, transition
import enum

class Managerassistant(TimeMixin):
    manager = models.ForeignKey(User, related_name="manager", on_delete=models.CASCADE)
    assistant = models.ForeignKey(User, related_name="manager_assistant", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at", )
        unique_together = (("manager", "assistant", "is_active"), )


class AssistantClient(TimeMixin):
    assistant = models.ForeignKey(User, related_name="client_assistant", on_delete=models.CASCADE)
    client = models.ForeignKey(User, related_name="client", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at", )
        unique_together = (("assistant", "client", "is_active"), )


class AttributeStatus(enum.Enum):
    PENDING = "Pending"
    REJECTED = "Rejected"
    APPROVED = "Approved"


class ClientAttributeTransaction(TimeMixin):
    assistant_client = models.ForeignKey(AssistantClient, related_name="assistant_client", on_delete=models.CASCADE)
    attribute_name = models.CharField(max_length=250, null=False, blank=False)
    attribute_old_value = models.CharField(max_length=250, null=False, blank=False)
    attribute_new_value = models.CharField(max_length=250, null=False, blank=False)
    status = FSMField(choices= [(choice.value, choice.name) for choice in AttributeStatus], default=AttributeStatus.PENDING)

    class Meta:
        ordering = ("-created_at", )

    @transition(field=status, source=AttributeStatus.PENDING, target=AttributeStatus.REJECTED)
    def reject(self):
        """
        """
        pass

    @transition(field=status, source=AttributeStatus.PENDING, target=AttributeStatus.APPROVED)
    def approve(self):
        """
        """
        pass





