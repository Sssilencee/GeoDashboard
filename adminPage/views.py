from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views import View
from django.shortcuts import redirect
from django.shortcuts import render

import json

import requests

from .forms import LicenseKeysForm
from .forms import InvitesForm

from .models import LicenseKeys
from .models import Invites
from .models import Groups
from .models import Admins
from .models import Devices
from .models import UnbindDiscordKeys


DISCORD_AUTH = 'https://discord.com/api/oauth2/authorize?client_id=857571464319860767&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2FnothingInteresting%2Flogin&response_type=code&scope=identify%20email%20guilds'
CLIENT_ID = ''
CLIENT_SECRET = ''

HOME_PAGE = 'http://127.0.0.1:8000/nothingInteresting'
LOGIN_PAGE = 'http://127.0.0.1:8000/nothingInteresting/login'


class Home(View):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):

        discord_data = request.session.get('adminData')

        # Check if user is already logined
        if discord_data:

            admin = Admins.objects.filter(
                discord_id = discord_data['id']
            )

            admin_groups = list(admin.values_list('group', flat = True))
            license_keys_data = self.get_license_keys(admin_groups)

            admin_key = list(admin.values_list('admin_key', flat = True))[0]

            return render(
                request,
                'adminPage/adminPage.html',
                {
                    'adminData': json.dumps(discord_data),
                    'groups': json.dumps(admin_groups),
                    'licenseKeysData': license_keys_data,
                    'invitesData': Invites.objects.all(),
                    'licenseKeysForm': LicenseKeysForm(),
                    'invitesForm': InvitesForm(),
                    'adminKey': admin_key
                }
            )

        else:
            return render(request, 'adminPage/adminPage.html')

    def post(self, request):

        admin_key = request.POST.get('admin_key')
        group = request.POST.get('group')

        user_groups = list(Admins.objects.filter(
            admin_key = admin_key
        ).values_list('group', flat = True))

        # Check if user has admin access
        if len(user_groups) == 0 or group not in user_groups:
            return redirect(HOME_PAGE)

        license_keys_form = InvitesForm(request.POST)
        if license_keys_form.is_valid():
            license_keys_form.save()

        invites_form = LicenseKeysForm(request.POST)
        if invites_form.is_valid():
            invites_form.save()

        return redirect(HOME_PAGE)

    def get_license_keys(self, admin_groups):

        license_keys_data = LicenseKeys.objects.filter(
            group__in = admin_groups
        ).order_by('-id')

        return license_keys_data


class Login(View):

    def get(self, request):

        code = request.GET.get('code')

        # Check if user was redirected from Discord OAuth with code
        if code:

            access_token = self.exchange_code(code)
            discord_data = self.get_discord_data(access_token)
            admins = list(Admins.objects.values_list('discord_id', flat = True))

            if discord_data.get('id') in admins:
                request.session['adminData'] = discord_data

            return redirect(HOME_PAGE)

        else:
            return redirect(DISCORD_AUTH)

    def exchange_code(self, code: str):

        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': LOGIN_PAGE,
            'scope': 'identify email guilds'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        credentials = requests.post(
            'https://discord.com/api/oauth2/token',
            data = data,
            headers = headers
        ).json()
        access_token = credentials['access_token']

        return access_token

    def get_discord_data(self, access_token):

        headers = {
            'Authorization': 'Bearer ' + access_token
        }

        discord_data = requests.get(
            'https://discord.com/api/v6/users/@me',
            headers = headers
        ).json()

        return discord_data


class Logout(View):

    def get(self, request):
        del request.session['adminData']
        return redirect(HOME_PAGE)


class Delete(View):

    def post(self, request):

        delete_key = request.headers['deleteKey']

        LicenseKeys.objects.filter(license_key = delete_key).delete()

        return redirect(HOME_PAGE)


class DeleteDiscord(View):

    def post(self, request):

        discord_id = request.headers['discordId']
        tool = request.headers['tool']
        key = request.headers['key']

        try:
            UnbindDiscordKeys.objects.get(key = key)
        except UnbindDiscordKeys.DoesNotExist:
            return JsonResponse({'status': 'error'})

        license_key = LicenseKeys.objects.get(
            discord_id = discord_id,
            tool = tool
        )
        license_key.delete()

        Devices.objects.filter(
            license_key = license_key.license_key
        ).delete()

        return JsonResponse({'status': 'success'})


class DeleteInvite(View):

    def post(self, request):

        delete_key = request.headers['deleteKey']

        Invites.objects.filter(public_link = delete_key).delete()

        return redirect(HOME_PAGE)
