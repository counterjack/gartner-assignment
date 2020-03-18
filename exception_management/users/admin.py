from django.contrib import admin

# Register your models here.


from users.models import AssistantClient, ClientAttributeTransaction, Managerassistant


admin.site.register(AssistantClient, list_display=(
    "assistant", "client", "is_active", "created_at", "updated_at"
    ))
admin.site.register(Managerassistant, list_display=(
    "assistant", "manager", "is_active", "created_at", "updated_at"
    ))
admin.site.register(ClientAttributeTransaction, list_display=(
    "assistant_client", "attribute_name", "attribute_old_value", "attribute_new_value" , "created_at", "updated_at"
    ))

