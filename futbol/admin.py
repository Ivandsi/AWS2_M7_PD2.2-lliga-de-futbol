from django.contrib import admin

# Register your models here.
from futbol.models import *

class EventInline(admin.TabularInline):
    model = Event
    extra = 2

class PartitAdmin(admin.ModelAdmin):
    list_display = ("equip_local", "equip_visitant", "data", "gols_local", "gols_visitant")
    inlines = [EventInline]

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)
admin.site.register(Partit, PartitAdmin)