from rest_framework import serializers

from .models import Tour, Transport

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ('description', 'start_date', 'end_date', 'transport', 'ticket_cost',
                  'home_cab_cost', 'dest_cab_cost', 'hotel_cost', 'status',)

