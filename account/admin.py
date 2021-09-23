from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models.signals import post_save


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


def SaveProfile(sender, **kwargs):
    if kwargs.get('created'):
        p1 = Profile(user=kwargs.get('instance'))
        p1.save()


post_save.connect(receiver=SaveProfile, sender=User)
