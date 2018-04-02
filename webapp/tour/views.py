from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from employee.models import Employee

from .forms import TourForm
from .models import Currency, Hotel, HotelCost, Tour, Ticket, Transport

@login_required(login_url='/accounts/login/')
def index(request):
    user = request.user
    employee = Employee.objects.get(user=user)
    is_worker = True if employee.employee_type == 'worker' else False
    form = TourForm()
    transports = Transport.objects.all()
    currencies = Currency.objects.all()
    hotels = Hotel.objects.all()
    managers = Employee.objects.filter(employee_type=Employee.MANAGER)

    if request.method == "GET":
        if is_worker:
            tour_list = Tour.objects.filter(worker=employee)
        else:
            if employee.employee_type == 'manager':
                tour_list = Tour.objects.filter(Q(status=Tour.SUBMITTED) |
                                                Q(status=Tour.REJECTED) |
                                                Q(status=Tour.REQUEST_FOR_INFORMATION) |
                                                Q(manager=employee))
            elif employee.employee_type == 'finance_manager':
                tour_list = Tour.objects.filter(Q(status=Tour.SUBMITTED) |
                                                Q(status=Tour.REJECTED) |
                                                Q(status=Tour.REQUEST_FOR_INFORMATION) |
                                                Q(manager__isNone=False))

    if request.method == "POST":
        if is_worker:
            tour_list = Tour.objects.filter(worker=employee)
            transports = Transport.objects.all()
            currencies = Currency.objects.all()
            hotels = Hotel.objects.all()
            managers = Employee.objects.filter(employee_type=Employee.MANAGER)

            description = request.POST.get("description")
            start_date = request.POST.get("startDate")
            end_date = request.POST.get("endDate")
            home_cab = request.POST.get("homeCab")
            dest_cab = request.POST.get("destCab")
            hotel = request.POST.get("hotel")
            hotel_currency = request.POST.get("hotelCurrency")
            hotel_cost = request.POST.get("hotelCost")
            transport_type = request.POST.get("transportType")
            transport_currency = request.POST.get("transportCurrency")
            transport_cost = request.POST.get("transportCost")
            status = Tour.DRAFT if request.POST.get("draft") else Tour.SUBMITTED
            manager = request.POST.get("approvingManager")
            
            hc = HotelCost.objects.create(hotel=Hotel.objects.get(name=hotel), currency=Currency.objects.get(currency=hotel_currency), cost=hotel_cost)
            ticket = Ticket.objects.create(transport=Transport.objects.get(name=transport_type), currency=Currency.objects.get(currency=transport_currency), cost=transport_cost)
            Tour.objects.create(description=description, start_date=start_date, end_date=end_date, home_cab=home_cab, dest_cab=dest_cab, hotel_cost=hc, ticket=ticket, status=status, worker=employee, manager=Employee.objects.get(pk=manager))

    context = {
        'tours': tour_list,
        'transport_types': transports,
        'currencies': currencies,
        'hotels': hotels,
        'is_worker': is_worker,
        'user': user,
        'form': form,
        'managers': managers,
    }

    return render(request, 'tour/index.html', context)
