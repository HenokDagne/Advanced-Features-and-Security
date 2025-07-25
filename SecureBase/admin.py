from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PremiumUser

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'bio', 'birth_date', 'profile_picture', 'is_staff', 'is_active')
    search_field = ('email', 'first_name', 'last_name', 'username')
    list_editable = ('username', 'email', 'first_name', 'last_name', 'bio', 'birth_date', 'profile_picture','is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'email')

    #Define the fieldsets for adding and changing users in the admin
    # this structure is similar to the default UserAdmin
    # but we add our custom fields
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'birth_date', 'profile_picture')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email',)
        }),
    )

@admin.register(PremiumUser)
class PremiumUserAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'membrership_start_date', 'membership_end_date', 'premium_features_enabled')
    search_fields = ('user__email',)
    list_filter = ('premium_features_enabled',)
    list_editable = ('user', 'membership_end_date', 'premium_features_enabled')


     
    