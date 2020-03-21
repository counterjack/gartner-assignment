# Generated by Django 3.0.4 on 2020-03-21 06:53

from django.db import migrations, transaction

def create_test_user_relation_data(apps, schema_editor):
    """[summary]

    Arguments:
        apps {[type]} -- [description]
        schema_editor {[type]} -- [description]
    """
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    ManagerAssociate = apps.get_model('users', 'ManagerAssociate')
    AssociateClient = apps.get_model('users', 'AssociateClient')
    manager_group = Group.objects.get(name="Manager")
    associate_group = Group.objects.get(name="Associate")
    client_group = Group.objects.get(name="Client")

    manager = User.objects.filter(groups=manager_group).first()
    associate = User.objects.filter(groups=associate_group).first()
    client = User.objects.filter(groups=client_group).first()

    with transaction.atomic():
        # Create manager andn associate mapping
        manager_associate = ManagerAssociate.objects.create(manager=manager, associate=associate)
        # create associate and client mapping
        associate_client = AssociateClient.objects.create(client=client, associate=associate)


def reverse_relation(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    ManagerAssociate = apps.get_model('users', 'ManagerAssociate')
    AssociateClient = apps.get_model('users', 'AssociateClient')
    manager_group = Group.objects.get(name="Manager")
    associate_group = Group.objects.get(name="Associate")
    client_group = Group.objects.get(name="Client")

    manager = User.objects.filter(groups=manager_group).first()
    associate = User.objects.filter(groups=associate_group).first()
    client = User.objects.filter(groups=client_group).first()

    ManagerAssociate.objects.filter(manager=manager, associate=associate).delete()
    AssociateClient.objects.filter(client=client, associate=associate).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_create_test_users'),
    ]

    operations = [
        migrations.RunPython(create_test_user_relation_data, reverse_relation)
    ]
