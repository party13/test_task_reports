from django import forms
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = ('username',  'is_active')


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'is_active', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('username',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.


    ordering = ('username',)
    filter_horizontal = ()


# Register your models here.
admin.register(User, UserAdmin)