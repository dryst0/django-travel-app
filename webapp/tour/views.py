from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

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
    finance_managers = Employee.objects.filter(employee_type=Employee.FINANCE_MANAGER)

    tour_list = None
    if is_worker:
        tour_list = Tour.objects.filter(worker=employee)
    else:
        if employee.employee_type == 'manager':
            tour_list = Tour.objects.filter(Q(status=Tour.SUBMITTED) |
                                            Q(status=Tour.REQUEST_FOR_INFORMATION) |
                                            Q(status=Tour.APPROVED),
                                            manager=employee)
        elif employee.employee_type == 'finance_manager':
            tour_list = Tour.objects.filter(Q(status=Tour.SUBMITTED) |
                                            Q(status=Tour.REQUEST_FOR_INFORMATION) |
                                            Q(status=Tour.APPROVED),
                                            manager__isNone=False)

    if request.method == "POST":
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
        manager = request.POST.get("approvingManager")
        hc = HotelCost.objects.create(hotel=Hotel.objects.get(name=hotel),
                                      currency=Currency.objects.get(currency=hotel_currency),
                                      cost=hotel_cost)
        ticket = Ticket.objects.create(transport=Transport.objects.get(name=transport_type),
                                       currency=Currency.objects.get(currency=transport_currency),
                                       cost=transport_cost)

        if request.POST.get("draft") or request.POST.get("update"):
            status = Tour.DRAFT
        elif request.POST.get("save") or request.POST.get("submit"):
            status = Tour.SUBMITTED
        elif request.POST.get("rfi"):
            status = Tour.REQUEST_FOR_INFORMATION
        elif request.POST.get("approve"):
            status = Tour.APPROVED
        elif request.POST.get("reject"):
            status = Tour.REJECTED

        if request.POST.get("tourId"):
            if is_worker:
                tour = Tour.objects.filter(pk=request.POST.get("tourId"))
                tour.update(description=description, start_date=start_date, end_date=end_date,
                            home_cab=home_cab, dest_cab=dest_cab, hotel_cost=hc, ticket=ticket,
                            status=status, worker=employee, manager=Employee.objects.get(pk=manager))
            else:
                tour = Tour.objects.filter(pk=request.POST.get("tourId"))
                tour.update(status=status)

            return redirect("/tours/")
        else:
            Tour.objects.create(description=description, start_date=start_date, end_date=end_date,
                                home_cab=home_cab, dest_cab=dest_cab, hotel_cost=hc, ticket=ticket,
                                status=status, worker=employee, manager=Employee.objects.get(pk=manager))

    context = {
        'tours': tour_list,
        'transport_types': transports,
        'currencies': currencies,
        'hotels': hotels,
        'is_worker': is_worker,
        'user': user,
        'form': form,
        'managers': managers,
        'finance_managers': finance_managers
    }

    return render(request, 'tour/index.html', context)
