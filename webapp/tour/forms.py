from django import forms

from .models import Tour

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['description', 'start_date', 'end_date', 'ticket', 'home_cab', 'dest_cab',
                  'hotel_cost', 'manager']
