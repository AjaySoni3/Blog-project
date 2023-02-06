from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render,redirect
class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", False)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        try:
            get_user_model().objects.get(email=sociallogin.user.email)
        except get_user_model().DoesNotExist:
            # raise ImmediateHttpResponse(redirect('login'))
            raise ImmediateHttpResponse(HttpResponse(status=500))
            # return render(request,'times/500.html',{})

        else:
            user = get_user_model().objects.get(email=sociallogin.user.email)
            if not sociallogin.is_existing:
                sociallogin.connect(request, user)