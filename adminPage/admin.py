from django.contrib import admin
from django.db import models
from django.forms import TextInput

from .models import LicenseKeys
from .models import Invites
from .models import Groups
from .models import Admins
from .models import Devices
from .models import UnbindDiscordKeys


@admin.register(LicenseKeys, Invites, Groups, Admins, Devices, UnbindDiscordKeys)
class PersonsAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={
                'autocomplete':'off',
                'class':'vTextField'
            })
        }
    }
