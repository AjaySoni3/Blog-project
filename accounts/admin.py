from django.contrib import admin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Reader, Author, ReaderAdditional, AuthorAdditional
from django.contrib.auth.admin import UserAdmin as AuthAdmin


# Register your models here.


class CustomUserAdmin(AuthAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Personal info', {'fields': ('user_type',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class ReaderAdditionalInline(admin.TabularInline):
    model = ReaderAdditional


class ReaderAdmin(admin.ModelAdmin):
    inlines = [ReaderAdditionalInline]

    list_display = ['email', 'username']
    list_filter = ('email', 'is_staff', 'is_active')

    search_fields = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Personal info', {'fields': ('user_type',)}),

    )


class AuthorAdditionalInline(admin.TabularInline):
    model = AuthorAdditional
    list_display = ['bio', 'profile_pic']


class AuthorAdmin(admin.ModelAdmin):
    inlines = [AuthorAdditionalInline]
    list_display = ['email', 'username']
    list_filter = ('email', 'is_staff', 'is_active')

    search_fields = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'username',)}),
        ('Personal info', {'fields': ('user_type',)}),

    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(ReaderAdditional)
admin.site.register(AuthorAdditional)
