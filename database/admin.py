from django.contrib import admin

from .models import Leader, Character, Stage, Event

admin.site.register(Leader)
admin.site.register(Character)
admin.site.register(Stage)
admin.site.register(Event)