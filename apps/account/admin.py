from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from apps.account.forms import UserChangeForm, UserCreationForm
from apps.account.models import MyUser, UserFollowing


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_staff','image')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password','user_name')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','image')}),
        (_('Permissions'), {'fields': ('is_staff','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'accept', 'created']


admin.site.register(UserFollowing, UserFollowingAdmin)
