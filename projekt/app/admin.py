from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.
#admin.site.register(Korisnik)
admin.site.register(Uloge)
admin.site.register(Predmet)
admin.site.register(Upisi)

@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('None', {'fields':('uloga', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('None', {'fields':('uloga', 'status')}),
    )
    