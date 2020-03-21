from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from  typing import List
from rest_framework.response import Response
# Create your views here.
from core.models import UserGroups
from core.view_mixins import LoginRequiredViewMixin
from users.serializers import (
    ActiveTransactionReviewSerializer, AssociateClientSerializer,
    UserSerializer, ManagerActionOnAttributeTransactionSerializer)
from users.models import AssociateClient, ManagerAssociate, ClientAttributeTransaction, AttributeStatus
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect, JsonResponse

from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import status
from users.forms import LoginForm
from django.views import View
from django.contrib.auth import logout
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form_data = LoginForm(request.POST)
        if form_data.is_valid():
            username = form_data.cleaned_data.get("username")
            password = form_data.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponsePermanentRedirect(redirect_to= reverse("users:dashboard"))

        return render(request, "users/login.html", context={
            "message": "Invalid username/Password",
            "status": status.HTTP_401_UNAUTHORIZED,
            "form": LoginForm()
        })


class LogoutView(LoginRequiredViewMixin):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponsePermanentRedirect(reverse("users:user-login"))


class DashboardRedirectAPI(LoginRequiredViewMixin):

    def get(self, request, *args, **kwargs):
        if (request.user.groups.all().first().name == UserGroups.Manager.value):
            return HttpResponsePermanentRedirect(redirect_to=reverse("users:manager-dashboard"))

        if (request.user.groups.all().first().name == UserGroups.Associate.value):
            return HttpResponsePermanentRedirect(redirect_to=reverse("users:associate-dashboard"))


class ManagerDashboardAPI(LoginRequiredViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # get the list of all the associate for current manager
        associates_ids: List[int] = ManagerAssociate.objects.filter(
            manager=request.user).values_list("associate_id", flat=True)

        active_transaction_reviews = ClientAttributeTransaction.objects.filter(
            associate_client__associate__id__in=associates_ids,
            status=AttributeStatus.PENDING.value)

        return render(request, "users/manager-dashboard.html", context = {
            "data": ActiveTransactionReviewSerializer(active_transaction_reviews, many=True).data
        })


class AssociateDashboardAPI(View):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # get the list of all the associate for current manager
        associate_clients: List[int] = AssociateClient.objects.filter(associate=request.user)
        return render(request, "users/associate-dashboard.html", context = {
            "data":AssociateClientSerializer(associate_clients, many=True).data})


class ClientAttributeTransactionView(LoginRequiredViewMixin):

    def post(self, request, *args, **kwargs):

        serialized_data = ManagerActionOnAttributeTransactionSerializer(data=request.POST)
        serialized_data.is_valid(raise_exception=True)

        validated_data = serialized_data.validated_data
        manager_id = validated_data.get("manager_id")
        transaction_id = validated_data.get("transaction_id")
        action =  validated_data.get("action")

        manager_associate = get_object_or_404(ManagerAssociate, manager_id=manager_id)
        transactions = ClientAttributeTransaction.objects.filter(
            id=transaction_id,
            associate_client__associate=manager_associate.associate
            )


        if transactions.exists():
            transaction = transactions.first()
            if (action == AttributeStatus.APPROVED.value):
                transaction.approve()
                # Now, Update the attribute of the client
                client = transaction.associate_client.client
                setattr(client, transaction.attribute_name, transaction.attribute_new_value)
                client.save()
            elif (action == AttributeStatus.REJECTED.value):
                transaction.reject()

            transaction.save()
            return JsonResponse({"message": "Success", "status": status.HTTP_200_OK})

        return JsonResponse({"message": "Invalid Transaction Id", "status": status.HTTP_403_FORBIDDEN})



