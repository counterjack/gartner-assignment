from django.contrib import admin

# Register your models here.


from users.models import AssociateClient, ClientAttributeTransaction, ManagerAssociate


admin.site.register(AssociateClient, list_display=(
    "associate", "client", "is_active", "created_at", "updated_at"
    ))
admin.site.register(ManagerAssociate, list_display=(
    "associate", "manager", "is_active", "created_at", "updated_at"
    ))
admin.site.register(ClientAttributeTransaction, list_display=(
    "associate_client", "attribute_name", "attribute_old_value", "status", "attribute_new_value" , "created_at", "updated_at"
    ))

