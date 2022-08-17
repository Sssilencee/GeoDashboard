from django.db import models


class LicenseKeys(models.Model):

    discord_id = models.CharField('discordId', max_length=50)
    license_key = models.CharField('licenseKey', max_length=20)
    tool = models.CharField('tool', max_length=50)

    devices = models.CharField('devices', max_length=100)

    group = models.CharField('group', max_length=50)
    admin_key = models.CharField('adminKey', max_length=50)

    def __str__(self):
        return self.discord_id

    class Meta:
        verbose_name = 'licenseKey'
        verbose_name_plural = 'licenseKeys'


class Invites(models.Model):

    private_link = models.CharField('privateLink', max_length=50)
    public_link = models.CharField('publicLink', max_length=50)

    group = models.CharField('group', max_length=50)
    admin_key = models.CharField('adminKey', max_length=50)

    def __str__(self):
        return self.public_link

    class Meta:
        verbose_name = 'invite'
        verbose_name_plural = 'invites'


class Groups(models.Model):

    group_name = models.CharField('groupName', max_length=50)

    renewal_price = models.CharField('renewalPrice', max_length=50)
    renewal_date = models.CharField('renewalDate', max_length=50)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Admins(models.Model):

    discord_id = models.CharField('discordId', max_length=50)

    group = models.CharField('group', max_length=50)
    admin_key = models.CharField('adminKey', max_length=50)

    def __str__(self):
        return self.discord_id

    class Meta:
        verbose_name = 'admin'
        verbose_name_plural = 'admins'


class Devices(models.Model):

    device_id = models.CharField('deviceId', max_length=100)
    license_key = models.CharField('licenseKey', max_length=20)

    def __str__(self):
        return self.device_id

    class Meta:
        verbose_name = 'device'
        verbose_name_plural = 'devices'


class UnbindDiscordKeys(models.Model):

    key = models.CharField('key', max_length=50)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'UnbindDiscordKey'
        verbose_name_plural = 'UnbindDiscordKeys'
