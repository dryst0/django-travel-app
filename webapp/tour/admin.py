from django.contrib import admin

from .models import Currency, Hotel, HotelCost, Ticket, Tour, Transport

admin.site.register(Currency)

admin.site.register(Hotel)

admin.site.register(HotelCost)

admin.site.register(Ticket)

admin.site.register(Tour)

admin.site.register(Transport)
