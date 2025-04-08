from django.contrib import admin

from .models import Leader, Character, Stage, Event, PriceHistory

admin.site.register(Leader)
admin.site.register(Character)
admin.site.register(Stage)
admin.site.register(Event)
admin.site.register(PriceHistory)