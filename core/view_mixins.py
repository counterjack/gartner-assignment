from django.views import View
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse

class LoginRequiredViewMixin(View):
    def setup(self, request, *args, **kwargs):
        # Check if the user is authenticated or not
        if not request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse("users:user-login"))
        """Initialize attributes shared by all view methods."""

        self.request = request
        self.args = args
        self.kwargs = kwargs