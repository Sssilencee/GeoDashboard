from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views import View
from django.shortcuts import redirect
from django.shortcuts import render

import json

import requests

import time

from adminPage.models import LicenseKeys
from adminPage.models import Invites
from adminPage.models import Groups
from adminPage.models import Admins
from adminPage.models import Devices
from adminPage.models import UnbindDiscordKeys


DISCORD_AUTH = 'https://discord.com/api/oauth2/authorize?client_id=857571464319860767&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Flogin&response_type=code&scope=identify%20guilds%20email'
CLIENT_ID = '857571464319860767'
CLIENT_SECRET = 'FByG_IPnCsSbyV8kaqovpgBj2E_5D9zL'

HOME_PAGE = 'http://127.0.0.1:8000'
LOGIN_PAGE = 'http://127.0.0.1:8000/login'


class Home(View):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):

        discord_data = request.session.get('userData')

        # Check if user is already logined
        if discord_data:

            user_subscriptions = self.get_user_subscriptions(discord_data)

            return render(
                request,
                'userPage/userPage.html',
                {
                    'userSubscriptions': json.dumps(user_subscriptions),
                    'userData': json.dumps(discord_data['userInfo'])
                }
            )

        else:
            return render(request, 'userPage/userPage.html')

    def get_user_subscriptions(
                self, discord_data,
                user_subscriptions = {}):

        groups = list(Groups.objects.values_list(
            'group_name',
            'renewal_price',
            'renewal_date'
        ))

        for group_data in groups:
            if group_data[0] in discord_data['guilds']:
                # ^ Sort user guilds with db data ^

                user_subscriptions[group_data[0]] = {
                    'id': discord_data['guilds'][group_data[0]]['id'],
                    'icon': discord_data['guilds'][group_data[0]]['icon'],
                    'renewalPrice': group_data[1],
                    'renewalDate': group_data[2],
                    'licenseKeys': {}
                }

        license_keys = list(LicenseKeys.objects.filter(
            discord_id = discord_data['userInfo']['id']
        ).values_list('license_key', 'tool', 'devices', 'group'))

        for license_key in license_keys:
            if license_key[3] in user_subscriptions:
                # ^ Append user keys to sorted guilds ^

                user_subscriptions[license_key[3]]['licenseKeys'][license_key[1]] = {
                    'licenseKey': license_key[0],
                    'devices': license_key[2]
                }

        return user_subscriptions


class Login(View):

    def get(self, request):

        code = request.GET.get('code')

        # Check if user was redirected from Discord OAuth with code
        if code:

            access_token = self.exchange_code(code)
            discord_data = self.get_discord_data(access_token)

            invite_code = request.session.get('inviteCode')

            if invite_code:

                # Returns render method
                result = self.check_invite(request, invite_code, discord_data)
                del request.session['inviteCode']

                return result

            else:
                request.session['userData'] = discord_data
                return redirect(HOME_PAGE)

        else:
            return redirect(DISCORD_AUTH)

    def check_invite(self, request, invite_code, discord_data):

        # Converts discord id to unix timestamp
        discord_id = bin(int(discord_data['userInfo']['id']))
        m = 42 - (64 - len(discord_id))
        creation_date_unix = int(discord_id[2:m], 2) + 1420070400000

        # Check if user account is burner
        if creation_date_unix < int(time.time() * 1000) - 15778463000:

            public_url = Invites.objects.filter(
                public_link = invite_code
            ).first()

            # Checks if invite code is valid
            if public_url:

                discord_url = list(Invites.objects.filter(
                    public_link = invite_code
                ).values_list('private_link', flat = True))[0]

                return redirect(discord_url)

            else:
                return render(
                    request,
                    'userPage/inviteError.html',
                    {'message': 'Code error'}
                )
        else:
            return render(
                request,
                'userPage/inviteError.html',
                {'message': 'Burner?'}
            )

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

    def get_discord_data(
                self, access_token,
                guilds = {}):

        headers = {
            'Authorization': 'Bearer ' + access_token
        }

        user_info = requests.get(
            'https://discord.com/api/v6/users/@me',
            headers = headers
        ).json()

        guilds_unsort = requests.get(
            'https://discord.com/api/v6/users/@me/guilds',
            headers = headers
        ).json()

        groups_registered = list(Groups.objects.values_list(
            'group_name',
            flat = True
        ))

        for guild in guilds_unsort:
            if guild['name'] in groups_registered:
                guilds[guild['name']] = {
                    'id': guild['id'],
                    'icon': guild['icon']
                }

        discord_data = {
            'guilds': guilds,
            'userInfo': user_info
        }

        return discord_data


class Logout(View):

    def get(self, request):
        del request.session['userData']
        return redirect(HOME_PAGE)


# Old versions wrong class name. "LicenseKey" - is correct.
class Api(View):

    # Old versions wrong method type. "POST" - is correct
    def get(self, request):

        key = request.headers['key']
        tool = request.headers['tool']
        device_id = request.headers['deviceId']

        devices_list = list(Devices.objects.filter(
            license_key = key
        ).values_list('device_id', flat = True))
        activation_limit = int(list(LicenseKeys.objects.filter(
            tool = tool,
            license_key = key
        ).values_list('devices', flat = True))[0].split('/')[1])
        # ^ Get activations from 0/1 format ^

        if device_id not in devices_list:
            if len(devices_list) < activation_limit:

                # Add new device to database
                Devices(device_id = device_id, license_key = key).save()
                LicenseKeys.objects.filter(
                    tool = tool,
                    license_key = key
                ).update(
                    devices = str(len(devices_list) + 1) + '/' + str(activation_limit)
                     # ^ Add new activation to key ^
                )

                is_valid = {'status': 'success'}

            else:
                is_valid = {'status': 'error'}

        else:
            is_valid = {'status': 'success'}

        return JsonResponse(is_valid)


class Invite(View):

    def get(self, request):

        invite_code = request.GET.get('code')

        request.session['inviteCode'] = invite_code

        return redirect(DISCORD_AUTH)


class Unbind(View):

    def get(self, request):

        key = request.headers['key']

        Devices.objects.filter(license_key = key).delete()
        LicenseKeys.objects.filter(
            license_key = key
        ).update(devices = '0/1')

        return JsonResponse({'status': 'success'})


class UnbindDiscord(View):

    def get(self, request):

        discord_id = request.headers['discordId']
        tool = request.headers['tool']
        key = request.headers['key']

        try:
            UnbindDiscordKeys.objects.get(key = key)
        except:
            return JsonResponse({'status': 'error'})

        license_key = LicenseKeys.objects.get(
            discord_id = discord_id,
            tool = tool
        )
        license_key.devices = '0/1'
        license_key.save()

        Devices.objects.filter(
            license_key = license_key.license_key
        ).delete()

        return JsonResponse({'status': 'success'})
