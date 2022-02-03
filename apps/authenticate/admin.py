from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'role')
    class Meta:
        model = CustomUser

# admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)