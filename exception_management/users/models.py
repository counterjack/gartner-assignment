from django.db import models
from core.models import TimeMixin, UserGroups
# Create your models here.
from django.contrib.auth.models import User
from django_fsm import FSMField, transition
import enum
from django.dispatch import receiver
from django.db.models.signals import pre_save
from rest_framework.exceptions import ValidationError


class ManagerAssociate(TimeMixin):
    manager = models.ForeignKey(User, related_name="manager", on_delete=models.CASCADE)
    associate = models.OneToOneField(User, related_name="manager_associate", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at", )
        unique_together = (("manager", "associate", "is_active"), )


@receiver(pre_save, sender=ManagerAssociate)
def validate_users_group_for_manager_associate(sender, instance, **kwargs):
    # validate manager

    if (instance.manager.groups.all().first().name != UserGroups.Manager.value):
        raise ValidationError("Invalid Manager role")
    # Validate associate
    if (instance.associate.groups.all().first().name != UserGroups.Associate.value):
        raise ValidationError("Invalid Associate role")


class AssociateClient(TimeMixin):
    associate = models.ForeignKey(User, related_name="client_associate", on_delete=models.CASCADE)
    client = models.OneToOneField(User, related_name="client", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at", )
        unique_together = (("associate", "client", "is_active"), )


@receiver(pre_save, sender=AssociateClient)
def validate_users_group_associate_client(sender, instance, **kwargs):
    # validate manager
    if (instance.client.groups.all().first().name != UserGroups.Client.value):
        raise ValidationError("Invalid Client role")

    if (instance.associate.groups.all().first().name != UserGroups.Associate.value):
        raise ValidationError("Invalid Assitant role")

class AttributeStatus(enum.Enum):
    PENDING = "Pending"
    REJECTED = "Rejected"
    APPROVED = "Approved"


class ClientAttributeTransaction(TimeMixin):
    associate_client = models.ForeignKey(AssociateClient, related_name="associate_client", on_delete=models.CASCADE)
    attribute_name = models.CharField(max_length=250, null=False, blank=False)
    attribute_old_value = models.CharField(max_length=250, null=False, blank=False)
    attribute_new_value = models.CharField(max_length=250, null=False, blank=False)
    status = FSMField(
        choices= [(choice.value, choice.name) for choice in AttributeStatus],
        default=AttributeStatus.PENDING,
        protected=True
        )

    class Meta:
        ordering = ("-created_at", )

    @transition(field=status, source=AttributeStatus.PENDING.value, target=AttributeStatus.REJECTED.value)
    def reject(self):
        """
        """
        pass

    @transition(field=status, source=AttributeStatus.PENDING.value, target=AttributeStatus.APPROVED.value)
    def approve(self):
        """
        """
        pass





