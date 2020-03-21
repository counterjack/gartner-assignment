from rest_framework import serializers
from users.models import ClientAttributeTransaction, AssociateClient, ManagerAssociate, AttributeStatus
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        exclude = ("password", "last_login", "is_superuser", "is_staff", "is_active")


class ManagerAssociateSerializer(serializers.ModelSerializer):
    nested_associate = serializers.SerializerMethodField(read_only=True)
    nested_manager = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = ManagerAssociate
        fields = "__all__"


    def get_nested_associate(self, obj):
        return UserSerializer(obj.associate).data

    def get_nested_manager(self, obj):
        return UserSerializer(obj.manager).data



class AssociateClientSerializer(serializers.ModelSerializer):
    nested_associate = serializers.SerializerMethodField(read_only=True)
    nested_client = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = AssociateClient
        exclude = ("created_at", "updated_at")


    def get_nested_associate(self, obj):
        return UserSerializer(obj.associate).data

    def get_nested_client(self, obj):
        return UserSerializer(obj.client).data


class ActiveTransactionReviewSerializer(serializers.ModelSerializer):
    nested_associate_client = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ClientAttributeTransaction
        fields = ("id", "associate_client", "attribute_name", "attribute_old_value", "attribute_new_value", "nested_associate_client", "created_at")

    def get_nested_associate_client(self, object):
        return AssociateClientSerializer(object.associate_client).data

class ManagerActionOnAttributeTransactionSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField(required=True)
    transaction_id = serializers.IntegerField(required=True)
    action = serializers.ChoiceField(choices=[(choice.value, choice.name) for choice in AttributeStatus if choice.value != AttributeStatus.PENDING.value])
 