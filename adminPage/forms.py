from django.forms import ModelForm, Select, TextInput, HiddenInput
from .models import LicenseKeys
from .models import Invites


class LicenseKeysForm(ModelForm):

    class Meta:
        model = LicenseKeys
        fields = ['discord_id', 'license_key', 'tool', 'devices', 'admin_key', 'group']
        widgets = {
            'discord_id': TextInput(attrs= {
                'type': 'text',
                'id': 'discordId',
                'class': 'inputKeyWindow',
                'placeholder': 'Discord id'
            }),
            'license_key': TextInput(attrs= {
                'type': 'text',
                'id': 'key',
                'class': 'inputKeyWindow',
                'placeholder': 'License key'
            }),
            'tool': TextInput(attrs= {
                'type': 'text',
                'id': 'tool',
                'class': 'inputKeyWindow',
                'placeholder': 'Tool'
            }),
            'devices': TextInput(attrs= {
                'type': 'text',
                'id': 'devices',
                'class': 'inputKeyWindow',
                'placeholder': 'Devices'
            }),
            'admin_key': TextInput(attrs= {
                'id': 'adminKey',
                'class': 'inputKeyWindow',
                'style': 'display: none;'
            }),
            'group': Select(attrs= {
                'id': 'group',
                'class': 'inputKeyWindow'
            })
        }


class InvitesForm(ModelForm):

    class Meta:
        model = Invites
        fields = ['private_link', 'public_link', 'admin_key', 'group']
        widgets = {
            'private_link': TextInput(attrs= {
                'type': 'text',
                'id': 'privateLink',
                'class': 'inputKeyWindow',
                'placeholder': 'Private link'
            }),
            'public_link': TextInput(attrs= {
                'type': 'text',
                'id': 'publicLink',
                'class': 'inputKeyWindow',
                'placeholder': 'Public link'
            }),
            'admin_key': TextInput(attrs= {
                'id': 'adminKeyInvite',
                'class': 'inputKeyWindow',
                'style': 'display: none;'
            }),
            'group': Select(attrs= {
                'id': 'groupInvite',
                'class': 'inputKeyWindow'
            })
        }
